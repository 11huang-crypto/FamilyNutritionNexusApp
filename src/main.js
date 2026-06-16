import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Button, Image as VantImage, Uploader, Divider, Tag, Cell, CellGroup, Card, Progress, List, Stepper, Checkbox, Icon, NavBar, Popup, Dialog, Toast, Loading, Swipe, SwipeItem } from 'vant'
import 'vant/lib/index.css'

const app = createApp(App)

app.use(router)

app.use(Button)
app.use(VantImage)
app.use(Uploader)
app.use(Divider)
app.use(Tag)
app.use(Cell)
app.use(CellGroup)
app.use(Card)
app.use(Progress)
app.use(List)
app.use(Stepper)
app.use(Checkbox)
app.use(Icon)
app.use(NavBar)
app.use(Popup)
app.use(Dialog)
app.use(Toast)
app.use(Loading)
app.use(Swipe)
app.use(SwipeItem)

app.mount('#app')