<template>
  <canvas ref="canvasRef" class="particle-bg"></canvas>
</template>

<script setup>
/**
 * ParticleBackground v4.1 — 规格化薄荷青粒子波浪
 *
 * 规格要点：
 * 1. 纯白底 #FFFFFF
 * 2. 三层分层：前景高密度细粒子 1-3px / 中层柔光 3-6px / 远景散景光斑 6-14px
 * 3. 低饱和薄荷青，半透明，柔光
 * 4. 10秒周期，柔和呼吸，少量淡入淡出
 * 5. 波峰密谷疏（正态分布初始化 + 透明度随波浪密度调整）
 */
import { ref, onMounted, onBeforeUnmount } from 'vue'

const canvasRef = ref(null)
let ctx = null
let animId = null
let allParticles = []   // 按层分组
let timeMs = 0
let lastTime = 0

// ============ 全局配置 ============
const CFG = {
  wavePeriod: 10000,   // 主周期 10s

  // 薄荷青色板（v4.2 — 更饱和更深，0x4FA882 为基底）
  mintColors: [
    [79,  168, 130],   // 深薄荷绿
    [108, 188, 152],   // 中薄荷
    [140, 200, 175],   // 浅薄荷
    [85,  170, 145],   // 暗薄荷
    [120, 190, 165],   // 柔薄荷
    [60,  155, 120],   // 墨薄荷
  ],

  layers: [
    // 前景（高频细粒子，波浪主体）
    {
      name: 'foreground',
      count: 700,
      radius: [1.5, 3.5],
      alpha: [0.45, 0.85],   // ← 大幅提高下限
      speed: 1.0,
      waveAmp: 60,
      waveLen: 600,
      yRange: [0.10, 0.90],
      densityCurve: true,
      breatheSpeed: 0.001,
      fadeCycle: 0.05,
    },
    // 中层（柔光粒子）
    {
      name: 'midground',
      count: 250,
      radius: [3.5, 7.0],
      alpha: [0.35, 0.70],   // ← 大幅提高
      speed: 0.6,
      waveAmp: 45,
      waveLen: 750,
      yRange: [0.08, 0.92],
      densityCurve: true,
      breatheSpeed: 0.0008,
      fadeCycle: 0.08,
    },
    // 远景（散景光斑）
    {
      name: 'background',
      count: 60,
      radius: [8.0, 18.0],
      alpha: [0.20, 0.45],   // ← 之前 0.05-0.18 太弱
      speed: 0.25,
      waveAmp: 30,
      waveLen: 900,
      yRange: [0.05, 0.95],
      densityCurve: false,
      breatheSpeed: 0.0005,
      fadeCycle: 0.15,
    },
  ],
}

class Particle {
  constructor(layerCfg, canvasW, canvasH, layerIndex) {
    this.layerCfg = layerCfg
    this.canvasW = canvasW
    this.canvasH = canvasH
    this.layerIndex = layerIndex

    this.phase = Math.random()

    if (layerCfg.densityCurve) {
      const u1 = Math.random(), u2 = Math.random()
      const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2)
      const peakIndex = Math.floor(Math.random() * 2)
      this.phase = (peakIndex * 0.5 + 0.125) + z * 0.08
      this.phase = ((this.phase % 1) + 1) % 1
    }

    const [rMin, rMax] = layerCfg.radius
    this.radius = rMin + Math.random() * (rMax - rMin)

    const colorIdx = Math.floor(Math.random() * CFG.mintColors.length)
    this.color = CFG.mintColors[colorIdx]

    const [aMin, aMax] = layerCfg.alpha
    this.baseAlpha = aMin + Math.random() * (aMax - aMin)

    this.breathePhase = Math.random() * Math.PI * 2
    this.breatheSpeed = layerCfg.breatheSpeed * (0.8 + Math.random() * 0.4)

    this.fadePhase = Math.random() * Math.PI * 2
    this.fadeSpeed = (Math.PI * 2 / (CFG.wavePeriod * (0.5 + Math.random()))) * 0.5
    this.hasFade = Math.random() < layerCfg.fadeCycle

    this.bobPhase = Math.random() * Math.PI * 2
    this.bobSpeed = 0.0006 + Math.random() * 0.001
    this.bobAmp = 1.5 + Math.random() * 3

    this.harmonicFactor = 0.15 + Math.random() * 0.25
    this.ySpread = (Math.random() - 0.5) * layerCfg.waveAmp * 0.3

    this.x = 0
    this.y = 0
    this.currentAlpha = this.baseAlpha
  }

  update(t) {
    const cfg = this.layerCfg
    const period = CFG.wavePeriod
    const t_norm = (t % period) / period

    const bandLen = this.canvasW * 1.4
    this.phase += (cfg.speed * 0.00008)
    if (this.phase > 1) this.phase -= 1

    this.x = (this.phase - 0.2) * bandLen

    const [yMin, yMax] = cfg.yRange
    const yCenter = this.canvasH * (yMin + (yMax - yMin) * (0.3 + 0.4 * Math.sin(this.phase * Math.PI)))

    const mainWave = Math.sin(
      this.phase * Math.PI * 2 * (bandLen / cfg.waveLen) +
      t_norm * Math.PI * 2 +
      this.layerIndex * 0.7
    ) * cfg.waveAmp

    const harmonic = Math.sin(
      this.phase * Math.PI * 2 * (bandLen / (cfg.waveLen * this.harmonicFactor)) +
      t_norm * Math.PI * 2 * 0.6 +
      this.layerIndex * 1.3
    ) * cfg.waveAmp * this.harmonicFactor

    const bob = Math.sin(t * this.bobSpeed + this.bobPhase) * this.bobAmp

    this.y = yCenter + mainWave + harmonic + this.ySpread + bob

    const breathe = 0.85 + 0.15 * Math.sin(t * this.breatheSpeed + this.breathePhase)

    let fadeAlpha = 1.0
    if (this.hasFade) {
      fadeAlpha = 0.6 + 0.4 * (0.5 + 0.5 * Math.sin(t * this.fadeSpeed + this.fadePhase))
    }

    this.currentAlpha = this.baseAlpha * breathe * fadeAlpha

    if (cfg.densityCurve) {
      const waveDensity = 0.5 + 0.5 * Math.abs(Math.sin(this.phase * Math.PI * 2 + t_norm * Math.PI * 2))
      this.currentAlpha *= (0.7 + 0.3 * waveDensity)
    }

    this.currentAlpha = Math.max(0.05, Math.min(0.95, this.currentAlpha))
  }

  draw(ctx) {
    const [r, g, b] = this.color
    const a = this.currentAlpha

    if (this.layerIndex === 2) {
      const glowR = this.radius * 4
      const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, glowR)
      gradient.addColorStop(0, `rgba(${r},${g},${b},${a})`)
      gradient.addColorStop(0.3, `rgba(${r},${g},${b},${a * 0.4})`)
      gradient.addColorStop(1, `rgba(${r},${g},${b},0)`)
      ctx.fillStyle = gradient
      ctx.beginPath()
      ctx.arc(this.x, this.y, glowR, 0, Math.PI * 2)
      ctx.fill()
    } else {
      if (this.radius > 2.5 && a > 0.15) {
        const glowR = this.radius * 2.5
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, glowR)
        gradient.addColorStop(0, `rgba(${r},${g},${b},${a})`)
        gradient.addColorStop(1, `rgba(${r},${g},${b},0)`)
        ctx.fillStyle = gradient
        ctx.beginPath()
        ctx.arc(this.x, this.y, glowR, 0, Math.PI * 2)
        ctx.fill()
      }

      ctx.beginPath()
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(${r},${g},${b},${a})`
      ctx.fill()
    }
  }
}

function init() {
  const w = canvasRef.value ? canvasRef.value.clientWidth : window.innerWidth
  const h = canvasRef.value ? canvasRef.value.clientHeight : window.innerHeight

  allParticles = []
  for (let li = 0; li < CFG.layers.length; li++) {
    const layerCfg = CFG.layers[li]
    const layerParticles = []
    for (let i = 0; i < layerCfg.count; i++) {
      layerParticles.push(new Particle(layerCfg, w, h, li))
    }
    allParticles.push(layerParticles)
  }

  console.log(
    `[粒子v4.1] 初始化完成 | 前景:${CFG.layers[0].count} | 中层:${CFG.layers[1].count} | 远景:${CFG.layers[2].count} | 总计:${CFG.layers.reduce((s,l)=>s+l.count,0)}`
  )
}

function render(timestamp) {
  if (!ctx) return
  if (!lastTime) lastTime = timestamp
  const dt = timestamp - lastTime
  lastTime = timestamp
  timeMs += dt

  ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)

  for (let li = allParticles.length - 1; li >= 0; li--) {
    const layer = allParticles[li]
    for (const p of layer) {
      p.update(timeMs)
      p.draw(ctx)
    }
  }

  animId = requestAnimationFrame(render)
}

function resize() {
  if (!canvasRef.value) return
  const dpr = window.devicePixelRatio || 1
  const w = window.innerWidth
  const h = window.innerHeight

  canvasRef.value.width = w * dpr
  canvasRef.value.height = h * dpr
  canvasRef.value.style.width = w + 'px'
  canvasRef.value.style.height = h + 'px'
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  init()
}

onMounted(() => {
  ctx = canvasRef.value.getContext('2d')
  resize()
  animId = requestAnimationFrame(render)
  window.addEventListener('resize', resize)
  console.log('[粒子v4.1] 启动 — 规格化版本')
})

onBeforeUnmount(() => {
  if (animId) cancelAnimationFrame(animId)
  window.removeEventListener('resize', resize)
})
</script>

<style scoped>
.particle-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
}
</style>
