from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Union
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "family-nutrition-nexus-secret-key-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./family-nutrition.db")

VISION_SERVICE_URL = os.getenv("VISION_SERVICE_URL", "http://localhost:8001")
MEAL_PLAN_SERVICE_URL = os.getenv("MEAL_PLAN_SERVICE_URL", "http://localhost:8002")
BAIDU_API_KEY = os.getenv("BAIDU_API_KEY", "")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY", "")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(title="家庭营养管理系统 API", version="1.0.0")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    reset_code = Column(String, nullable=True)
    reset_code_expire = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Family(Base):
    __tablename__ = "families"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    invite_code = Column(String, nullable=True, unique=True)
    invite_code_expire = Column(DateTime, nullable=True)
    admin = relationship("User", back_populates="families")


class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)


class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Float, default=1.0)
    unit = Column(String, default="个")
    checked = Column(Boolean, default=False)
    added_by = Column(Integer, ForeignKey("users.id"))
    added_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class HealthProfile(Base):
    __tablename__ = "health_profiles"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    conditions = Column(Text)
    allergens = Column(Text)
    taboos = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class BasketItem(Base):
    __tablename__ = "basket_items"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    ingredient_name = Column(String, nullable=False)
    quantity = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)


class FamilyInvitation(Base):
    __tablename__ = "family_invitations"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    inviter_id = Column(Integer, ForeignKey("users.id"))
    invitee_email = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


User.families = relationship("Family", back_populates="admin")

Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @field_validator("password")
    def password_must_not_contain_chinese(cls, v):
        if any('\u4e00' <= c <= '\u9fff' for c in v):
            raise ValueError("密码不能包含中文")
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None


class FamilyCreate(BaseModel):
    name: str


class FamilyJoinRequest(BaseModel):
    invite_code: str


class FamilyResponse(BaseModel):
    id: int
    name: str
    admin_id: int

    class Config:
        from_attributes = True


class FamilyMemberResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True


class InviteRequest(BaseModel):
    email: EmailStr


class HealthProfileCreate(BaseModel):
    family_id: int
    name: str
    conditions: List[str] = Field(default_factory=list)
    allergens: List[str] = Field(default_factory=list)
    taboos: List[str] = Field(default_factory=list)


class HealthProfileUpdate(BaseModel):
    name: Optional[str] = None
    conditions: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    taboos: Optional[List[str]] = None


class HealthProfileResponse(BaseModel):
    id: int
    family_id: int
    user_id: int
    name: str
    conditions: List[str]
    allergens: List[str]
    taboos: List[str] = []

    class Config:
        from_attributes = True


class BasketItemCreate(BaseModel):
    family_id: int
    ingredient_name: str
    quantity: Optional[str] = None


class BasketItemResponse(BaseModel):
    id: int
    family_id: int
    user_id: int
    ingredient_name: str
    quantity: Optional[str]
    added_at: datetime

    class Config:
        from_attributes = True


class RiskWarning(BaseModel):
    type: str
    severity: str
    message: str
    related_items: List[str]


class BasketCheckResponse(BaseModel):
    warnings: List[RiskWarning]
    total_items: int
    risk_count: int


class NutritionInfo(BaseModel):
    calories: Optional[float]
    protein: Optional[float]
    fat: Optional[float]
    carbs: Optional[float]
    fiber: Optional[float]
    vitamins: Optional[dict]


class IngredientAnalysis(BaseModel):
    name: str
    confidence: float
    nutrition: NutritionInfo


class MatchingRecommendation(BaseModel):
    ingredient: str
    reason: str
    type: str


class AnalysisResponse(BaseModel):
    ingredients: List[IngredientAnalysis]
    recommendations: List[MatchingRecommendation]


class MealPlanDay(BaseModel):
    day: str
    breakfast: str
    lunch: str
    dinner: str
    snacks: Optional[List[str]]


class MealPlanResponse(BaseModel):
    week: str
    meals: List[MealPlanDay]


class ShoppingItem(BaseModel):
    name: str
    quantity: str
    category: str
    purchased: bool


class ShoppingListResponse(BaseModel):
    items: List[ShoppingItem]
    last_updated: datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证身份凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/auth/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(new_user)
    }


@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }


@app.post("/auth/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该邮箱未注册"
        )
    
    reset_code = str(random.randint(100000, 999999))
    db.query(User).filter(User.email == email).update({
        "reset_code": reset_code,
        "reset_code_expire": datetime.now() + timedelta(minutes=30)
    })
    db.commit()
    
    print(f"验证码已发送到邮箱: {email}, 验证码: {reset_code}")
    
    return {"message": "验证码已发送到您的邮箱"}


@app.post("/auth/reset-password")
def reset_password(email: str, code: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该邮箱未注册"
        )
    
    if user.reset_code != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误"
        )
    
    if user.reset_code_expire and user.reset_code_expire < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码已过期"
        )
    
    hashed_password = get_password_hash(new_password)
    db.query(User).filter(User.email == email).update({
        "password": hashed_password,
        "reset_code": None,
        "reset_code_expire": None
    })
    db.commit()
    
    return {"message": "密码重置成功"}


@app.post("/family/create", response_model=FamilyResponse)
def create_family(
    family: FamilyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_family = Family(name=family.name, admin_id=current_user.id)
    db.add(new_family)
    db.commit()
    db.refresh(new_family)
    
    new_member = FamilyMember(
        family_id=new_family.id,
        user_id=current_user.id,
        role="admin"
    )
    db.add(new_member)
    db.commit()
    
    return FamilyResponse.model_validate(new_family)


@app.get("/family/my")
def get_my_families(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    memberships = db.query(FamilyMember).filter(
        FamilyMember.user_id == current_user.id
    ).all()
    
    families = []
    for member in memberships:
        family = db.query(Family).filter(Family.id == member.family_id).first()
        if family:
            families.append({
                "id": family.id,
                "name": family.name,
                "admin_id": family.admin_id,
                "role": member.role
            })
    
    return {"families": families}


@app.post("/family/{family_id}/invite")
def invite_member(
    family_id: int,
    invite: InviteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member or member.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以邀请成员"
        )
    
    invitee = db.query(User).filter(User.email == invite.email).first()
    if not invitee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该邮箱对应的用户不存在"
        )
    
    existing_member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == invitee.id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户已是家庭成员"
        )
    
    new_invitation = FamilyInvitation(
        family_id=family_id,
        inviter_id=current_user.id,
        invitee_email=invite.email,
        status="pending"
    )
    db.add(new_invitation)
    db.commit()
    db.refresh(new_invitation)
    
    return {"message": "邀请已发送", "invitation_id": new_invitation.id}


@app.get("/family/{family_id}/members")
def get_family_members(
    family_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    members = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id
    ).all()
    
    result = []
    for m in members:
        user = db.query(User).filter(User.id == m.user_id).first()
        if user:
            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": m.role,
                "joined_at": m.joined_at
            })
    
    return {"members": result}


@app.post("/family/{family_id}/generate-code")
def generate_invite_code(
    family_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member or member.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以生成邀请码"
        )
    
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家庭不存在"
        )
    
    import random
    import string
    while True:
        invite_code = ''.join(random.choices(string.digits, k=6))
        existing = db.query(Family).filter(Family.invite_code == invite_code).first()
        if not existing:
            break
    
    family.invite_code = invite_code
    family.invite_code_expire = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    db.refresh(family)
    
    return {
        "message": "邀请码已生成",
        "invite_code": invite_code,
        "expire_time": family.invite_code_expire
    }


@app.post("/family/join")
def join_family(
    req: FamilyJoinRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    family = db.query(Family).filter(Family.invite_code == req.invite_code).first()
    
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="邀请码无效"
        )
    
    if family.invite_code_expire and family.invite_code_expire < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邀请码已过期"
        )
    
    existing_member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family.id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已是该家庭的成员"
        )
    
    new_member = FamilyMember(
        family_id=family.id,
        user_id=current_user.id,
        role="member"
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return {"message": "成功加入家庭", "family_id": family.id, "family_name": family.name}


@app.post("/health/profile", response_model=HealthProfileResponse)
def create_health_profile(
    profile: HealthProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == profile.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    new_profile = HealthProfile(
        family_id=profile.family_id,
        user_id=0,
        name=profile.name,
        conditions=json.dumps(profile.conditions),
        allergens=json.dumps(profile.allergens),
        taboos=json.dumps(profile.taboos) if profile.taboos else '[]'
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return HealthProfileResponse(
        id=new_profile.id,
        family_id=new_profile.family_id,
        user_id=new_profile.user_id,
        name=new_profile.name,
        conditions=json.loads(new_profile.conditions),
        allergens=json.loads(new_profile.allergens),
        taboos=json.loads(new_profile.taboos) if new_profile.taboos else []
    )


@app.get("/health/family/{family_id}")
def get_family_health_profiles(
    family_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    profiles = db.query(HealthProfile).filter(
        HealthProfile.family_id == family_id
    ).all()
    
    result = []
    for p in profiles:
        result.append({
            "id": p.id,
            "family_id": p.family_id,
            "user_id": p.user_id,
            "name": p.name,
            "conditions": json.loads(p.conditions),
            "allergens": json.loads(p.allergens),
            "taboos": json.loads(p.taboos) if p.taboos else [],
            "created_at": p.created_at,
            "updated_at": p.updated_at
        })
    
    return {"profiles": result}


@app.put("/health/profile/{profile_id}")
def update_health_profile(
    profile_id: int,
    profile: HealthProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"DEBUG: update_health_profile called with profile_id={profile_id}")
    print(f"DEBUG: profile data: name={profile.name}, conditions={profile.conditions}, allergens={profile.allergens}, taboos={profile.taboos}")
    print(f"DEBUG: name is None: {profile.name is None}")
    print(f"DEBUG: conditions is None: {profile.conditions is None}")
    print(f"DEBUG: allergens is None: {profile.allergens is None}")
    print(f"DEBUG: taboos is None: {profile.taboos is None}")
    
    existing_profile = db.query(HealthProfile).filter(
        HealthProfile.id == profile_id
    ).first()
    
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康档案不存在"
        )
    
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == existing_profile.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有权限"
        )
    
    if profile.name is not None:
        existing_profile.name = profile.name
    if profile.conditions is not None:
        existing_profile.conditions = json.dumps(profile.conditions)
    if profile.allergens is not None:
        existing_profile.allergens = json.dumps(profile.allergens)
    if profile.taboos is not None:
        existing_profile.taboos = json.dumps(profile.taboos)
    existing_profile.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(existing_profile)
    
    return {
        "id": existing_profile.id,
        "family_id": existing_profile.family_id,
        "user_id": existing_profile.user_id,
        "name": existing_profile.name,
        "conditions": json.loads(existing_profile.conditions),
        "allergens": json.loads(existing_profile.allergens),
        "taboos": json.loads(existing_profile.taboos) if existing_profile.taboos else []
    }


@app.delete("/health/profile/{profile_id}")
def delete_health_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_profile = db.query(HealthProfile).filter(
        HealthProfile.id == profile_id
    ).first()
    
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康档案不存在"
        )
    
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == existing_profile.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有权限"
        )
    
    db.delete(existing_profile)
    db.commit()
    
    return {"message": "健康档案删除成功"}


@app.post("/basket/item", response_model=BasketItemResponse)
def add_basket_item(
    item: BasketItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == item.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    new_item = BasketItem(
        family_id=item.family_id,
        user_id=current_user.id,
        ingredient_name=item.ingredient_name,
        quantity=item.quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return BasketItemResponse.model_validate(new_item)


@app.get("/basket/family/{family_id}")
def get_basket_items(
    family_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    items = db.query(BasketItem).filter(
        BasketItem.family_id == family_id
    ).order_by(BasketItem.added_at.desc()).all()
    
    return {"items": [BasketItemResponse.model_validate(item) for item in items]}


@app.put("/basket/item/{item_id}")
def update_basket_item(
    item_id: int,
    item: BasketItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_item = db.query(BasketItem).filter(BasketItem.id == item_id).first()
    
    if not existing_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="菜篮子项目不存在"
        )
    
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == existing_item.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有权限"
        )
    
    existing_item.ingredient_name = item.ingredient_name if item.ingredient_name else existing_item.ingredient_name
    existing_item.quantity = item.quantity if item.quantity else existing_item.quantity
    
    db.commit()
    db.refresh(existing_item)
    
    return {"message": "菜篮子项目更新成功"}


@app.delete("/basket/item/{item_id}")
def delete_basket_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(BasketItem).filter(BasketItem.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == item.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有权限"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "菜篮子项目删除成功"}


forbidden_combinations = [
    {"items": ["菠菜", "豆腐"], "message": "菠菜与豆腐同食可能影响钙吸收", "severity": "medium"},
    {"items": ["海鲜", "啤酒"], "message": "海鲜配啤酒易诱发痛风", "severity": "high"},
    {"items": ["柿子", "螃蟹"], "message": "柿子与螃蟹同食可能导致肠胃不适", "severity": "medium"},
    {"items": ["牛奶", "巧克力"], "message": "牛奶与巧克力同食可能影响消化", "severity": "low"},
]

allergy_map = {
    "花生": ["花生油", "花生酱"],
    "虾": ["虾", "虾仁", "虾皮"],
    "蟹": ["蟹", "螃蟹", "蟹黄"],
    "牛奶": ["牛奶", "奶酪", "黄油", "酸奶"],
    "鸡蛋": ["鸡蛋", "蛋", "蛋黄", "蛋清"],
    "小麦": ["小麦", "面粉", "面条", "面包"],
}

condition_avoid_map = {
    "痛风": ["海鲜", "啤酒", "动物内脏", "肉汤", "沙丁鱼", "凤尾鱼"],
    "肾结石": ["菠菜", "苋菜", "甜菜", "巧克力", "浓茶"],
}


@app.get("/basket/check", response_model=BasketCheckResponse)
def check_basket(
    family_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    items = db.query(BasketItem).filter(BasketItem.family_id == family_id).all()
    profiles = db.query(HealthProfile).filter(HealthProfile.family_id == family_id).all()
    
    ingredient_names = [item.ingredient_name for item in items]
    warnings = []
    
    for combo in forbidden_combinations:
        found = all(
            any(name.lower().find(item.lower()) != -1 for name in ingredient_names)
            for item in combo["items"]
        )
        if found:
            warnings.append({
                "type": "combination",
                "severity": combo["severity"],
                "message": combo["message"],
                "related_items": combo["items"]
            })
    
    for profile in profiles:
        allergens = eval(profile.allergens)
        conditions = eval(profile.conditions)
        
        for allergen in allergens:
            related_items = allergy_map.get(allergen, [allergen])
            for item in related_items:
                if any(name.lower().find(item.lower()) != -1 for name in ingredient_names):
                    warnings.append({
                        "type": "allergy",
                        "severity": "high",
                        "message": f"{profile.name} 对 {allergen} 过敏，菜篮子中含有相关成分",
                        "related_items": [item]
                    })
                    break
        
        for condition in conditions:
            avoid_items = condition_avoid_map.get(condition, [])
            for item in avoid_items:
                if any(name.lower().find(item.lower()) != -1 for name in ingredient_names):
                    warnings.append({
                        "type": "condition",
                        "severity": "medium",
                        "message": f"{profile.name} 有 {condition}，建议避免 {item}",
                        "related_items": [item]
                    })
    
    return {
        "warnings": warnings,
        "total_items": len(items),
        "risk_count": len(warnings)
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    image_content = await image.read()
    
    food_aliases = {
        '马铃薯': '土豆', '洋芋': '土豆',
        '西红柿': '番茄',
        '洋葱头': '洋葱',
        '青椒': '辣椒', '甜椒': '辣椒',
        '大头菜': '白菜', '大白菜': '白菜',
        '卷心菜': '白菜', '圆白菜': '白菜',
        '菠菜': '菠菜',
        '生菜': '生菜',
        '黄瓜': '黄瓜',
        '冬瓜': '冬瓜',
        '南瓜': '南瓜',
        '茄子': '茄子',
        '胡萝卜': '胡萝卜',
        '白萝卜': '萝卜', '青萝卜': '萝卜',
        '莲藕': '莲藕',
        '山药': '山药',
        '西兰花': '西兰花', '花菜': '西兰花', '菜花': '西兰花',
        '蘑菇': '蘑菇', '香菇': '蘑菇', '平菇': '蘑菇',
        '苹果': '苹果',
        '香蕉': '香蕉',
        '橙子': '橙子', '桔子': '橙子',
        '葡萄': '葡萄',
        '草莓': '草莓',
        '西瓜': '西瓜',
        '梨': '梨',
        '桃子': '桃子',
        '芒果': '芒果',
        '鸡蛋': '鸡蛋',
        '牛奶': '牛奶',
        '米饭': '米饭',
        '猪肉': '猪肉',
        '牛肉': '牛肉',
        '鸡肉': '鸡肉',
        '鱼': '鱼', '鱼肉': '鱼',
        '虾': '虾',
        '豆腐': '豆腐',
        '坚果': '坚果', '核桃': '坚果', '杏仁': '坚果', '花生': '坚果'
    }
    
    nutrition_db = {
        '番茄': {'calories': 18, 'protein': 0.9, 'fat': 0.2, 'carbs': 3.9, 'fiber': 1.2, 'vitamins': {'C': 13.7, 'A': 42}},
        '胡萝卜': {'calories': 41, 'protein': 0.9, 'fat': 0.2, 'carbs': 9.6, 'fiber': 2.8, 'vitamins': {'A': 835, 'K': 13.2}},
        '西兰花': {'calories': 34, 'protein': 2.8, 'fat': 0.4, 'carbs': 6.6, 'fiber': 2.6, 'vitamins': {'C': 89.2, 'K': 101}},
        '黄瓜': {'calories': 15, 'protein': 0.8, 'fat': 0.2, 'carbs': 2.9, 'fiber': 0.5, 'vitamins': {'C': 9.7, 'K': 16.4}},
        '土豆': {'calories': 77, 'protein': 2.6, 'fat': 0.2, 'carbs': 17.8, 'fiber': 1.6, 'vitamins': {'C': 14.1, 'B6': 0.21}},
        '洋葱': {'calories': 40, 'protein': 1.1, 'fat': 0.1, 'carbs': 9.0, 'fiber': 1.7, 'vitamins': {'C': 7.4, 'B6': 0.15}},
        '辣椒': {'calories': 25, 'protein': 1.0, 'fat': 0.4, 'carbs': 5.8, 'fiber': 2.1, 'vitamins': {'C': 144, 'A': 130}},
        '茄子': {'calories': 25, 'protein': 1.1, 'fat': 0.2, 'carbs': 5.9, 'fiber': 1.3, 'vitamins': {'C': 5.3, 'B6': 0.22}},
        '白菜': {'calories': 15, 'protein': 1.0, 'fat': 0.1, 'carbs': 3.2, 'fiber': 0.8, 'vitamins': {'C': 14.0, 'K': 57}},
        '菠菜': {'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 4.0, 'fiber': 2.2, 'vitamins': {'C': 28.1, 'K': 540}},
        '生菜': {'calories': 16, 'protein': 1.3, 'fat': 0.2, 'carbs': 2.9, 'fiber': 1.3, 'vitamins': {'C': 4.0, 'K': 126}},
        '蘑菇': {'calories': 26, 'protein': 3.1, 'fat': 0.3, 'carbs': 4.1, 'fiber': 2.5, 'vitamins': {'B2': 0.32, 'B3': 3.8}},
        '南瓜': {'calories': 26, 'protein': 0.7, 'fat': 0.1, 'carbs': 6.5, 'fiber': 0.8, 'vitamins': {'A': 148, 'C': 8.0}},
        '苹果': {'calories': 52, 'protein': 0.3, 'fat': 0.2, 'carbs': 14.0, 'fiber': 2.4, 'vitamins': {'C': 4.6, 'K': 2.2}},
        '香蕉': {'calories': 89, 'protein': 1.1, 'fat': 0.3, 'carbs': 22.8, 'fiber': 2.6, 'vitamins': {'B6': 0.36, 'C': 8.7}},
        '橙子': {'calories': 47, 'protein': 0.9, 'fat': 0.2, 'carbs': 11.7, 'fiber': 2.4, 'vitamins': {'C': 53.2, 'A': 11}},
        '葡萄': {'calories': 69, 'protein': 0.7, 'fat': 0.2, 'carbs': 18.1, 'fiber': 0.9, 'vitamins': {'C': 3.2, 'K': 14}},
        '草莓': {'calories': 32, 'protein': 0.7, 'fat': 0.3, 'carbs': 7.7, 'fiber': 2.0, 'vitamins': {'C': 58.8, 'K': 2.2}},
        '西瓜': {'calories': 30, 'protein': 0.6, 'fat': 0.1, 'carbs': 7.6, 'fiber': 0.4, 'vitamins': {'C': 8.1, 'A': 48}},
        '梨': {'calories': 57, 'protein': 0.4, 'fat': 0.2, 'carbs': 15.4, 'fiber': 3.1, 'vitamins': {'C': 4.0, 'K': 3.0}},
        '桃子': {'calories': 39, 'protein': 0.9, 'fat': 0.1, 'carbs': 9.5, 'fiber': 1.5, 'vitamins': {'C': 6.0, 'A': 31}},
        '芒果': {'calories': 60, 'protein': 0.8, 'fat': 0.4, 'carbs': 14.9, 'fiber': 1.6, 'vitamins': {'A': 54, 'C': 36.4}},
        '鸡蛋': {'calories': 143, 'protein': 13.0, 'fat': 9.5, 'carbs': 1.0, 'fiber': 0, 'vitamins': {'A': 600, 'D': 40}},
        '牛奶': {'calories': 65, 'protein': 3.2, 'fat': 3.2, 'carbs': 4.8, 'fiber': 0, 'vitamins': {'A': 34, 'D': 2.5}},
        '米饭': {'calories': 130, 'protein': 2.7, 'fat': 0.3, 'carbs': 28.0, 'fiber': 0.4, 'vitamins': {'B1': 0.11, 'B2': 0.05}},
        '猪肉': {'calories': 395, 'protein': 20.2, 'fat': 37.0, 'carbs': 0, 'fiber': 0, 'vitamins': {'B1': 0.53, 'B6': 0.37}},
        '牛肉': {'calories': 288, 'protein': 26.4, 'fat': 20.2, 'carbs': 0, 'fiber': 0, 'vitamins': {'B12': 2.4, 'B6': 0.54}},
        '鸡肉': {'calories': 167, 'protein': 19.3, 'fat': 9.4, 'carbs': 0, 'fiber': 0, 'vitamins': {'B6': 0.36, 'B12': 0.24}},
        '鱼': {'calories': 123, 'protein': 20.0, 'fat': 3.8, 'carbs': 0, 'fiber': 0, 'vitamins': {'B12': 1.4, 'D': 10}},
        '虾': {'calories': 80, 'protein': 18.6, 'fat': 0.8, 'carbs': 2.8, 'fiber': 0, 'vitamins': {'B12': 2.7, 'D': 3.5}},
        '豆腐': {'calories': 70, 'protein': 8.1, 'fat': 3.7, 'carbs': 4.2, 'fiber': 0.4, 'vitamins': {'B1': 0.06, 'B2': 0.06}},
        '坚果': {'calories': 654, 'protein': 20.0, 'fat': 60.0, 'carbs': 11.0, 'fiber': 8.0, 'vitamins': {'E': 4.0, 'B6': 0.6}},
        '莲藕': {'calories': 77, 'protein': 2.6, 'fat': 0.2, 'carbs': 17.2, 'fiber': 2.2, 'vitamins': {'C': 44.2, 'B6': 0.19}},
        '冬瓜': {'calories': 12, 'protein': 0.4, 'fat': 0.2, 'carbs': 2.6, 'fiber': 0.7, 'vitamins': {'C': 18.0, 'K': 1.0}},
        '山药': {'calories': 51, 'protein': 1.9, 'fat': 0.2, 'carbs': 11.6, 'fiber': 0.8, 'vitamins': {'C': 5.0, 'B6': 0.15}},
        '萝卜': {'calories': 23, 'protein': 0.9, 'fat': 0.1, 'carbs': 5.5, 'fiber': 1.0, 'vitamins': {'C': 16.0, 'K': 7.0}}
    }
    
    food_conflicts = {
        '土豆': [{'food': '香蕉', 'reason': '同食容易引起面部生斑，建议间隔2小时以上食用'}],
        '番茄': [{'food': '土豆', 'reason': '同食可能导致消化不良，胃肠功能弱的人需注意'}],
        '菠菜': [{'food': '豆腐', 'reason': '菠菜中的草酸与豆腐中的钙结合形成草酸钙，影响钙吸收，建议菠菜焯水后再食用'}],
        '鸡蛋': [{'food': '豆浆', 'reason': '豆浆中的胰蛋白酶抑制剂会影响鸡蛋蛋白质的吸收，建议豆浆煮熟后再搭配鸡蛋'}],
        '牛奶': [{'food': '橘子', 'reason': '牛奶中的蛋白质与橘子中的果酸结合，影响消化，建议喝完牛奶1小时后再吃橘子'}],
        '猪肉': [{'food': '田螺', 'reason': '同食容易引起腹痛腹泻，脾胃虚寒者尤其需要注意'}],
        '牛肉': [{'food': '栗子', 'reason': '同食不易消化，可能引起呕吐，建议分开食用或少量同食'}],
        '虾': [{'food': '维生素C', 'reason': '虾中的五价砷与维生素C反应生成有毒的三价砷，建议吃完虾2小时内不要大量食用含维C的食物'}],
        '鱼': [{'food': '羊肉', 'reason': '同食可能引起消化不良，两种肉类蛋白质含量都很高，建议适量搭配'}],
        '豆腐': [{'food': '蜂蜜', 'reason': '同食可能引起腹泻，尤其是肠胃敏感人群需要注意'}],
        '洋葱': [{'food': '蜂蜜', 'reason': '同食可能引起眼睛不适，建议间隔一段时间食用'}],
        '西兰花': [{'food': '牛奶', 'reason': '西兰花中的草酸与牛奶中的钙结合，影响钙吸收，建议焯水后食用'}],
        '胡萝卜': [{'food': '白萝卜', 'reason': '胡萝卜中的维生素C分解酶会破坏白萝卜中的维生素C，建议不要一起生吃'}],
        '苹果': [{'food': '海鲜', 'reason': '苹果中的鞣酸与海鲜中的蛋白质结合，不易消化，建议间隔一段时间食用'}],
        '香蕉': [{'food': '芋头', 'reason': '同食容易引起腹胀，两种食物都含有较多膳食纤维'}],
        '葡萄': [{'food': '海鲜', 'reason': '葡萄中的鞣酸与海鲜中的蛋白质结合，可能引起肠胃不适'}],
        '西瓜': [{'food': '羊肉', 'reason': '一冷一热，同食容易引起肠胃不适，体质虚寒者尤其注意'}],
        '梨': [{'food': '螃蟹', 'reason': '同食容易引起腹泻，两者都偏寒凉'}],
        '芒果': [{'food': '大蒜', 'reason': '同食可能引起皮肤过敏，尤其是敏感体质人群需要注意'}],
        '鸡肉': [{'food': '大蒜', 'reason': '同食可能影响消化，建议烹饪时大蒜用量不宜过多'}],
        '米饭': [{'food': '红薯', 'reason': '同食容易引起腹胀，两者都含有较多淀粉'}],
        '坚果': [{'food': '白酒', 'reason': '同食容易上火，尤其是体质偏热人群需要注意'}],
        '蘑菇': [{'food': '酒', 'reason': '同食可能引起中毒反应，尤其是野生蘑菇，严禁酒后食用'}],
        '莲藕': [{'food': '白萝卜', 'reason': '同食可能引起腹泻，两者都偏寒凉'}]
    }
    
    food_pairs = {
        '土豆': [
            {'food': '牛肉', 'reason': '土豆吸收牛肉汤汁更美味，营养均衡，经典搭配', 'type': '营养搭配'},
            {'food': '番茄', 'reason': '番茄土豆汤是经典家常菜，酸甜可口，开胃消食', 'type': '美味搭配'},
            {'food': '鸡蛋', 'reason': '土豆丝炒鸡蛋，营养丰富，口感鲜嫩', 'type': '营养搭配'},
            {'food': '青椒', 'reason': '青椒土豆丝，口感爽脆，下饭神器', 'type': '美味搭配'}
        ],
        '番茄': [
            {'food': '鸡蛋', 'reason': '番茄炒蛋，经典营养搭配，维生素C和蛋白质互补', 'type': '营养搭配'},
            {'food': '牛腩', 'reason': '番茄牛腩，酸甜口感，营养丰富', 'type': '美味搭配'},
            {'food': '豆腐', 'reason': '番茄豆腐汤，清淡可口，适合减脂期', 'type': '营养搭配'},
            {'food': '洋葱', 'reason': '番茄洋葱炒蛋，口感丰富，抗氧化效果好', 'type': '营养搭配'}
        ],
        '胡萝卜': [
            {'food': '羊肉', 'reason': '胡萝卜炖羊肉，营养滋补，胡萝卜素促进羊肉消化', 'type': '营养搭配'},
            {'food': '排骨', 'reason': '胡萝卜排骨汤，清甜可口，补钙又护眼', 'type': '营养搭配'},
            {'food': '鸡肉', 'reason': '胡萝卜炒鸡丁，营养均衡，色彩丰富', 'type': '美味搭配'},
            {'food': '玉米', 'reason': '胡萝卜玉米排骨汤，口感清甜，膳食纤维丰富', 'type': '营养搭配'}
        ],
        '西兰花': [
            {'food': '虾仁', 'reason': '西兰花炒虾仁，高蛋白低脂肪，减脂佳品', 'type': '营养搭配'},
            {'food': '牛肉', 'reason': '西兰花炒牛肉，维生素和蛋白质互补', 'type': '营养搭配'},
            {'food': '蒜蓉', 'reason': '蒜蓉西兰花，简单美味，保留营养', 'type': '美味搭配'},
            {'food': '胡萝卜', 'reason': '西兰花胡萝卜拼盘，色彩丰富，营养多样', 'type': '营养搭配'}
        ],
        '黄瓜': [
            {'food': '鸡蛋', 'reason': '黄瓜炒蛋，清爽可口，适合夏天', 'type': '美味搭配'},
            {'food': '木耳', 'reason': '黄瓜炒木耳，口感爽脆，清肠减脂', 'type': '营养搭配'},
            {'food': '豆腐', 'reason': '黄瓜豆腐汤，清淡解渴，适合夏天', 'type': '营养搭配'},
            {'food': '火腿肠', 'reason': '黄瓜炒火腿，简单快捷，下饭神器', 'type': '美味搭配'}
        ],
        '洋葱': [
            {'food': '牛肉', 'reason': '洋葱炒牛肉，香气四溢，促进食欲', 'type': '美味搭配'},
            {'food': '鸡蛋', 'reason': '洋葱炒蛋，口感丰富，营养均衡', 'type': '营养搭配'},
            {'food': '土豆', 'reason': '洋葱土豆泥，口感细腻，营养丰富', 'type': '美味搭配'},
            {'food': '番茄', 'reason': '洋葱番茄汤，酸甜开胃，适合晚餐', 'type': '美味搭配'}
        ],
        '菠菜': [
            {'food': '猪肝', 'reason': '菠菜猪肝汤，补铁补血，营养丰富', 'type': '营养搭配'},
            {'food': '鸡蛋', 'reason': '菠菜鸡蛋汤，简单快捷，营养均衡', 'type': '营养搭配'},
            {'food': '粉丝', 'reason': '菠菜拌粉丝，清爽可口，适合凉菜', 'type': '美味搭配'},
            {'food': '豆腐', 'reason': '菠菜豆腐汤，清淡营养，菠菜需焯水去除草酸', 'type': '营养搭配'}
        ],
        '白菜': [
            {'food': '猪肉', 'reason': '白菜猪肉饺子，经典搭配，鲜美可口', 'type': '美味搭配'},
            {'food': '豆腐', 'reason': '白菜豆腐汤，清淡营养，适合减脂期', 'type': '营养搭配'},
            {'food': '粉丝', 'reason': '白菜炒粉丝，简单美味，下饭神器', 'type': '美味搭配'},
            {'food': '虾仁', 'reason': '白菜虾仁汤，清淡鲜美，营养丰富', 'type': '营养搭配'}
        ],
        '蘑菇': [
            {'food': '鸡肉', 'reason': '蘑菇炖鸡汤，鲜香滋补，营养丰富', 'type': '营养搭配'},
            {'food': '青菜', 'reason': '蘑菇炒青菜，清淡爽口，营养均衡', 'type': '营养搭配'},
            {'food': '鸡蛋', 'reason': '蘑菇炒鸡蛋，鲜香可口，蛋白质丰富', 'type': '美味搭配'},
            {'food': '豆腐', 'reason': '蘑菇豆腐汤，清淡营养，适合素食者', 'type': '营养搭配'}
        ],
        '茄子': [
            {'food': '肉末', 'reason': '肉末茄子，经典下饭，口感软糯', 'type': '美味搭配'},
            {'food': '豆角', 'reason': '茄子烧豆角，口感丰富，家常美味', 'type': '美味搭配'},
            {'food': '番茄', 'reason': '番茄烧茄子，酸甜可口，开胃消食', 'type': '美味搭配'},
            {'food': '青椒', 'reason': '青椒炒茄子，口感爽脆，色彩丰富', 'type': '美味搭配'}
        ],
        '青椒': [
            {'food': '土豆', 'reason': '青椒土豆丝，经典家常菜，口感爽脆', 'type': '美味搭配'},
            {'food': '肉丝', 'reason': '青椒肉丝，香辣可口，下饭神器', 'type': '美味搭配'},
            {'food': '鸡蛋', 'reason': '青椒炒蛋，简单快捷，营养均衡', 'type': '营养搭配'},
            {'food': '木耳', 'reason': '青椒木耳炒肉，口感丰富，营养多样', 'type': '营养搭配'}
        ],
        '南瓜': [
            {'food': '小米', 'reason': '南瓜小米粥，养胃健脾，营养丰富', 'type': '营养搭配'},
            {'food': '排骨', 'reason': '南瓜排骨汤，清甜可口，营养滋补', 'type': '营养搭配'},
            {'food': '糯米', 'reason': '南瓜糯米饭，香甜软糯，口感丰富', 'type': '美味搭配'},
            {'food': '鸡蛋', 'reason': '南瓜炒鸡蛋，香甜可口，营养均衡', 'type': '美味搭配'}
        ],
        '莲藕': [
            {'food': '排骨', 'reason': '莲藕排骨汤，清甜滋补，口感粉糯', 'type': '营养搭配'},
            {'food': '绿豆', 'reason': '莲藕绿豆汤，清热解暑，适合夏天', 'type': '营养搭配'},
            {'food': '红枣', 'reason': '莲藕红枣汤，补血养颜，适合女性', 'type': '营养搭配'},
            {'food': '排骨', 'reason': '莲藕炒肉片，口感爽脆，营养丰富', 'type': '美味搭配'}
        ],
        '冬瓜': [
            {'food': '排骨', 'reason': '冬瓜排骨汤，清淡解暑，适合夏天', 'type': '营养搭配'},
            {'food': '虾米', 'reason': '虾米冬瓜汤，鲜香可口，补钙佳品', 'type': '美味搭配'},
            {'food': '丸子', 'reason': '冬瓜丸子汤，口感软糯，营养均衡', 'type': '美味搭配'},
            {'food': '海带', 'reason': '冬瓜海带汤，清热利湿，适合减脂期', 'type': '营养搭配'}
        ],
        '山药': [
            {'food': '排骨', 'reason': '山药排骨汤，健脾养胃，营养滋补', 'type': '营养搭配'},
            {'food': '红枣', 'reason': '山药红枣粥，补气养血，适合早餐', 'type': '营养搭配'},
            {'food': '鸡肉', 'reason': '山药炖鸡汤，清香滋补，口感细腻', 'type': '营养搭配'},
            {'food': '小米', 'reason': '山药小米粥，养胃健脾，适合肠胃不适人群', 'type': '营养搭配'}
        ],
        '萝卜': [
            {'food': '排骨', 'reason': '萝卜排骨汤，清甜解腻，营养丰富', 'type': '营养搭配'},
            {'food': '牛肉', 'reason': '萝卜炖牛肉，营养滋补，口感软糯', 'type': '营养搭配'},
            {'food': '虾皮', 'reason': '萝卜虾皮汤，鲜香补钙，适合儿童', 'type': '美味搭配'},
            {'food': '豆腐', 'reason': '萝卜豆腐汤，清淡营养，适合减脂期', 'type': '营养搭配'}
        ],
        '苹果': [
            {'food': '酸奶', 'reason': '苹果酸奶沙拉，酸甜可口，助消化', 'type': '营养搭配'},
            {'food': '燕麦', 'reason': '苹果燕麦粥，营养丰富，适合早餐', 'type': '营养搭配'},
            {'food': '梨', 'reason': '苹果梨汁，清甜解渴，维生素丰富', 'type': '营养搭配'},
            {'food': '香蕉', 'reason': '苹果香蕉奶昔，口感顺滑，能量满满', 'type': '美味搭配'}
        ],
        '香蕉': [
            {'food': '牛奶', 'reason': '香蕉牛奶，口感顺滑，助眠安神', 'type': '营养搭配'},
            {'food': '燕麦', 'reason': '香蕉燕麦粥，能量满满，适合运动后', 'type': '营养搭配'},
            {'food': '核桃', 'reason': '香蕉核桃奶昔，补脑益智，营养丰富', 'type': '营养搭配'},
            {'food': '酸奶', 'reason': '香蕉酸奶，酸甜可口，助消化', 'type': '美味搭配'}
        ],
        '橙子': [
            {'food': '酸奶', 'reason': '橙子酸奶，酸甜可口，维生素C丰富', 'type': '营养搭配'},
            {'food': '蜂蜜', 'reason': '橙子蜂蜜汁，润肺止咳，适合感冒', 'type': '营养搭配'},
            {'food': '苹果', 'reason': '橙子苹果汁，清爽解渴，维生素丰富', 'type': '营养搭配'},
            {'food': '沙拉', 'reason': '橙子水果沙拉，色彩丰富，口感清新', 'type': '美味搭配'}
        ],
        '葡萄': [
            {'food': '酸奶', 'reason': '葡萄酸奶，酸甜可口，助消化', 'type': '营养搭配'},
            {'food': '苹果', 'reason': '葡萄苹果沙拉，口感丰富，维生素多样', 'type': '营养搭配'},
            {'food': '蜂蜜', 'reason': '葡萄蜂蜜汁，润肺生津，口感清甜', 'type': '营养搭配'},
            {'food': '奶酪', 'reason': '葡萄奶酪拼盘，口感丰富，适合下午茶', 'type': '美味搭配'}
        ],
        '草莓': [
            {'food': '酸奶', 'reason': '草莓酸奶，酸甜可口，颜值高', 'type': '美味搭配'},
            {'food': '奶油', 'reason': '草莓奶油蛋糕，口感丰富，甜品经典', 'type': '美味搭配'},
            {'food': '香蕉', 'reason': '草莓香蕉奶昔，口感顺滑，维生素丰富', 'type': '营养搭配'},
            {'food': '燕麦', 'reason': '草莓燕麦碗，营养丰富，适合早餐', 'type': '营养搭配'}
        ],
        '西瓜': [
            {'food': '薄荷', 'reason': '西瓜薄荷汁，清凉解暑，适合夏天', 'type': '美味搭配'},
            {'food': '柠檬', 'reason': '西瓜柠檬汁，清爽解渴，维生素C丰富', 'type': '营养搭配'},
            {'food': '酸奶', 'reason': '西瓜酸奶，酸甜可口，解暑佳品', 'type': '美味搭配'},
            {'food': '冰块', 'reason': '冰镇西瓜，清凉解暑，夏日必备', 'type': '美味搭配'}
        ],
        '梨': [
            {'food': '冰糖', 'reason': '冰糖雪梨，润肺止咳，适合秋冬', 'type': '营养搭配'},
            {'food': '银耳', 'reason': '雪梨银耳汤，美容养颜，滋阴润燥', 'type': '营养搭配'},
            {'food': '蜂蜜', 'reason': '雪梨蜂蜜水，润肺生津，口感清甜', 'type': '营养搭配'},
            {'food': '百合', 'reason': '雪梨百合粥，清心安神，适合睡眠不好的人', 'type': '营养搭配'}
        ],
        '桃子': [
            {'food': '酸奶', 'reason': '桃子酸奶，酸甜可口，口感丰富', 'type': '美味搭配'},
            {'food': '蜂蜜', 'reason': '桃子蜂蜜汁，润肺生津，口感清甜', 'type': '营养搭配'},
            {'food': '燕麦', 'reason': '桃子燕麦粥，营养丰富，适合早餐', 'type': '营养搭配'},
            {'food': '蓝莓', 'reason': '桃子蓝莓沙拉，色彩丰富，抗氧化', 'type': '营养搭配'}
        ],
        '芒果': [
            {'food': '酸奶', 'reason': '芒果酸奶，香甜可口，口感顺滑', 'type': '美味搭配'},
            {'food': '糯米', 'reason': '芒果糯米饭，香甜软糯，经典甜品', 'type': '美味搭配'},
            {'food': '椰汁', 'reason': '芒果椰汁西米露，口感丰富，甜品经典', 'type': '美味搭配'},
            {'food': '香蕉', 'reason': '芒果香蕉奶昔，口感顺滑，能量满满', 'type': '营养搭配'}
        ],
        '鸡蛋': [
            {'food': '番茄', 'reason': '番茄炒蛋，经典营养搭配', 'type': '营养搭配'},
            {'food': '菠菜', 'reason': '菠菜鸡蛋汤，简单快捷，营养均衡', 'type': '营养搭配'},
            {'food': '牛奶', 'reason': '牛奶鸡蛋羹，口感细腻，营养丰富', 'type': '营养搭配'},
            {'food': '洋葱', 'reason': '洋葱炒蛋，口感丰富，营养均衡', 'type': '美味搭配'}
        ],
        '牛奶': [
            {'food': '燕麦', 'reason': '牛奶燕麦粥，营养丰富，适合早餐', 'type': '营养搭配'},
            {'food': '香蕉', 'reason': '香蕉牛奶，口感顺滑，助眠安神', 'type': '营养搭配'},
            {'food': '鸡蛋', 'reason': '牛奶鸡蛋羹，口感细腻，营养丰富', 'type': '营养搭配'},
            {'food': '可可', 'reason': '热可可牛奶，温暖香甜，适合冬天', 'type': '美味搭配'}
        ],
        '猪肉': [
            {'food': '白菜', 'reason': '白菜猪肉饺子，经典搭配，鲜美可口', 'type': '美味搭配'},
            {'food': '土豆', 'reason': '土豆红烧肉，经典家常菜，软糯香甜', 'type': '美味搭配'},
            {'food': '青椒', 'reason': '青椒肉丝，香辣可口，下饭神器', 'type': '美味搭配'},
            {'food': '莲藕', 'reason': '莲藕炖排骨，清甜滋补，口感丰富', 'type': '营养搭配'}
        ],
        '牛肉': [
            {'food': '土豆', 'reason': '土豆炖牛肉，经典搭配，营养均衡', 'type': '营养搭配'},
            {'food': '西兰花', 'reason': '西兰花炒牛肉，维生素和蛋白质互补', 'type': '营养搭配'},
            {'food': '胡萝卜', 'reason': '胡萝卜炖牛肉，营养滋补，口感丰富', 'type': '营养搭配'},
            {'food': '洋葱', 'reason': '洋葱炒牛肉，香气四溢，促进食欲', 'type': '美味搭配'}
        ],
        '鸡肉': [
            {'food': '蘑菇', 'reason': '蘑菇炖鸡汤，鲜香滋补，营养丰富', 'type': '营养搭配'},
            {'food': '土豆', 'reason': '土豆烧鸡，经典家常菜，口感丰富', 'type': '美味搭配'},
            {'food': '胡萝卜', 'reason': '胡萝卜炒鸡丁，营养均衡，色彩丰富', 'type': '营养搭配'},
            {'food': '青椒', 'reason': '青椒炒鸡肉，香辣可口，下饭神器', 'type': '美味搭配'}
        ],
        '鱼': [
            {'food': '豆腐', 'reason': '鱼头豆腐汤，营养丰富，口感鲜美', 'type': '营养搭配'},
            {'food': '萝卜', 'reason': '萝卜丝鲫鱼汤，清甜解腻，营养丰富', 'type': '营养搭配'},
            {'food': '西兰花', 'reason': '西兰花蒸鱼，清淡健康，营养均衡', 'type': '营养搭配'},
            {'food': '姜葱', 'reason': '姜葱蒸鱼，去腥增香，口感鲜美', 'type': '美味搭配'}
        ],
        '虾': [
            {'food': '西兰花', 'reason': '西兰花炒虾仁，高蛋白低脂肪，减脂佳品', 'type': '营养搭配'},
            {'food': '豆腐', 'reason': '虾仁豆腐汤，清淡鲜美，营养丰富', 'type': '营养搭配'},
            {'food': '黄瓜', 'reason': '黄瓜炒虾仁，清爽可口，营养均衡', 'type': '美味搭配'},
            {'food': '粉丝', 'reason': '蒜蓉粉丝蒸虾，鲜香可口，宴席必备', 'type': '美味搭配'}
        ],
        '豆腐': [
            {'food': '番茄', 'reason': '番茄豆腐汤，清淡可口，适合减脂期', 'type': '营养搭配'},
            {'food': '青菜', 'reason': '青菜豆腐汤，清淡营养，适合素食者', 'type': '营养搭配'},
            {'food': '蘑菇', 'reason': '蘑菇豆腐汤，清淡营养，口感丰富', 'type': '营养搭配'},
            {'food': '鸡蛋', 'reason': '豆腐炒鸡蛋，营养均衡，口感丰富', 'type': '美味搭配'}
        ],
        '坚果': [
            {'food': '酸奶', 'reason': '坚果酸奶，口感丰富，营养多样', 'type': '营养搭配'},
            {'food': '燕麦', 'reason': '坚果燕麦粥，能量满满，适合早餐', 'type': '营养搭配'},
            {'food': '水果', 'reason': '坚果水果沙拉，口感丰富，抗氧化', 'type': '营养搭配'},
            {'food': '牛奶', 'reason': '坚果牛奶，口感顺滑，营养丰富', 'type': '美味搭配'}
        ],
        '米饭': [
            {'food': '番茄炒蛋', 'reason': '经典搭配，下饭神器', 'type': '美味搭配'},
            {'food': '红烧肉', 'reason': '米饭配红烧肉，软糯香甜，经典组合', 'type': '美味搭配'},
            {'food': '咖喱', 'reason': '咖喱饭，香气四溢，口感丰富', 'type': '美味搭配'},
            {'food': '蒸鱼', 'reason': '米饭配蒸鱼，清淡健康，营养均衡', 'type': '营养搭配'}
        ]
    }
    
    def get_normalized_name(name):
        return food_aliases.get(name, name)
    
    def get_nutrition(name):
        normalized_name = get_normalized_name(name)
        return nutrition_db.get(normalized_name, nutrition_db.get(name, {
            'calories': 0, 'protein': 0, 'fat': 0, 
            'carbs': 0, 'fiber': 0, 'vitamins': {}
        }))
    
    def get_conflicts(name):
        normalized_name = get_normalized_name(name)
        return food_conflicts.get(normalized_name, [])
    
    def get_pairs(name):
        normalized_name = get_normalized_name(name)
        return food_pairs.get(normalized_name, [])
    
    async def analyze_with_baidu():
        if not BAIDU_API_KEY or not BAIDU_SECRET_KEY:
            raise HTTPException(status_code=503, detail="百度AI API密钥未配置")
        
        import base64
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 获取百度AI access token
            token_response = await client.post(
                "https://aip.baidubce.com/oauth/2.0/token",
                params={
                    "grant_type": "client_credentials",
                    "client_id": BAIDU_API_KEY,
                    "client_secret": BAIDU_SECRET_KEY
                }
            )
            token_data = token_response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise HTTPException(status_code=503, detail="获取百度AI token失败")
            
            # 同时调用菜品识别和果蔬识别API
            results = []
            
            # 1. 菜品识别API
            try:
                dish_response = await client.post(
                    "https://aip.baidubce.com/rest/2.0/image-classify/v2/dish",
                    params={"access_token": access_token},
                    data={"image": image_base64, "top_num": 5}
                )
                dish_result = dish_response.json()
                print(f"菜品识别结果: {dish_result}")
                if dish_result.get("result"):
                    for item in dish_result.get("result", []):
                        name = item.get("name", "")
                        if name != "非菜":  # 过滤掉"非菜"结果
                            probability = float(item.get("probability", 0))
                            results.append({"name": name, "confidence": probability, "source": "菜品识别"})
            except Exception as e:
                print(f"菜品识别失败: {e}")
            
            # 2. 果蔬识别API
            try:
                plant_response = await client.post(
                    "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant",
                    params={"access_token": access_token},
                    data={"image": image_base64, "top_num": 5}
                )
                plant_result = plant_response.json()
                print(f"果蔬识别结果: {plant_result}")
                if plant_result.get("result"):
                    for item in plant_result.get("result", []):
                        name = item.get("name", "")
                        probability = float(item.get("probability", 0))
                        results.append({"name": name, "confidence": probability, "source": "果蔬识别"})
            except Exception as e:
                print(f"果蔬识别失败: {e}")
            
            # 3. 通用物体识别API（作为备选）
            try:
                general_response = await client.post(
                    "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general",
                    params={"access_token": access_token},
                    data={"image": image_base64}
                )
                general_result = general_response.json()
                print(f"通用物体识别结果: {general_result}")
                if general_result.get("result"):
                    for item in general_result.get("result", []):
                        name = item.get("keyword", "")
                        probability = float(item.get("score", item.get("probability", 0)))
                        results.append({"name": name, "confidence": probability, "source": "通用识别"})
            except Exception as e:
                print(f"通用识别失败: {e}")
            
            # 按置信度排序，取最优结果
            results.sort(key=lambda x: x["confidence"], reverse=True)
            print(f"所有识别结果排序: {results}")
            
            # 转换为最终格式
            ingredients = []
            seen_names = set()
            for item in results[:5]:
                name = item["name"]
                normalized_name = get_normalized_name(name)
                if normalized_name in seen_names:
                    continue
                seen_names.add(normalized_name)
                
                confidence = int(item["confidence"] * 100)
                nutrition = get_nutrition(name)
                
                ingredients.append({
                    "name": name,
                    "confidence": confidence,
                    "nutrition": nutrition
                })
            
            recommendations = []
            for item in ingredients[:3]:
                pairs = get_pairs(item['name'])
                if pairs:
                    for pair in pairs[:2]:
                        recommendations.append({
                            "ingredient": item['name'],
                            "food": pair['food'],
                            "reason": pair['reason'],
                            "type": pair['type']
                        })
                else:
                    rec_type = "营养搭配"
                    reason = "营养丰富，建议适量食用"
                    if item['nutrition'].get('vitamins', {}).get('C', 0) > 50:
                        reason = f"{item['name']}富含维生素C，抗氧化能力强"
                    elif item['nutrition'].get('protein', 0) > 20:
                        reason = f"{item['name']}蛋白质含量高，适合补充营养"
                    elif item['nutrition'].get('fiber', 0) > 2:
                        reason = f"{item['name']}膳食纤维丰富，促进消化"
                    recommendations.append({
                        "ingredient": item['name'],
                        "reason": reason,
                        "type": rec_type
                    })
            
            # 添加食物相克建议
            conflicts = []
            for item in ingredients[:3]:
                item_conflicts = get_conflicts(item['name'])
                if item_conflicts:
                    conflicts.extend([{
                        "ingredient": item['name'],
                        "food": c['food'],
                        "reason": c['reason'],
                        "type": "食物相克"
                    } for c in item_conflicts])
            
            return {"ingredients": ingredients, "recommendations": recommendations + conflicts}
    
    async def analyze_with_local_service():
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{VISION_SERVICE_URL}/analyze",
                files={"image": (image.filename, image_content, image.content_type)}
            )
            response.raise_for_status()
            return response.json()
    
    def get_mock_data():
        return {
            "ingredients": [
                {"name": "番茄", "confidence": 95, "nutrition": nutrition_db['番茄']},
                {"name": "胡萝卜", "confidence": 88, "nutrition": nutrition_db['胡萝卜']},
                {"name": "西兰花", "confidence": 92, "nutrition": nutrition_db['西兰花']}
            ],
            "recommendations": [
                {"ingredient": "番茄", "reason": "富含维生素C，适合搭配鸡蛋", "type": "营养搭配"},
                {"ingredient": "胡萝卜", "reason": "富含β-胡萝卜素，建议烹饪后食用", "type": "食用建议"},
                {"ingredient": "西兰花", "reason": "膳食纤维丰富，推荐清炒或焯水", "type": "烹饪建议"}
            ]
        }
    
    try:
        return await analyze_with_baidu()
    except Exception as e:
        print(f"百度AI识别失败，尝试本地服务: {e}")
        try:
            return await analyze_with_local_service()
        except Exception as e2:
            print(f"本地服务也失败，使用模拟数据: {e2}")
            return get_mock_data()


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend_py'))

from mock_data import RECIPES


@app.get("/recipes/{recipe_id}")
async def get_recipe_detail(recipe_id: str, current_user: User = Depends(get_current_user)):
    recipe = RECIPES.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="食谱不存在")
    return recipe


@app.get("/recipes/search")
async def search_recipes(
    keyword: str = "",
    ingredient: str = "",
    meal_type: str = "",
    current_user: User = Depends(get_current_user)
):
    results = []
    for recipe in RECIPES.values():
        match = True
        
        if keyword and keyword not in recipe["name"]:
            match = False
        
        if ingredient:
            has_ingredient = any(ingredient in item["name"] for item in recipe["ingredients"])
            if not has_ingredient:
                match = False
        
        if meal_type and meal_type not in recipe["meal_type"]:
            match = False
        
        if match:
            results.append(recipe)
    
    return {"recipes": results}


@app.post("/meal-plan/generate", response_model=MealPlanResponse)
async def generate_meal_plan(
    family_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    profiles = db.query(HealthProfile).filter(HealthProfile.family_id == family_id).all()
    
    health_restrictions = []
    for profile in profiles:
        allergens = eval(profile.allergens)
        conditions = eval(profile.conditions)
        health_restrictions.extend(allergens)
        health_restrictions.extend(conditions)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MEAL_PLAN_SERVICE_URL}/meal-plan/generate",
                json={
                    "family_id": family_id,
                    "health_restrictions": list(set(health_restrictions))
                }
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"食谱生成服务暂时不可用: {str(e)}"
        )


@app.get("/shopping-list/realtime")
async def get_shopping_list_realtime(
    family_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    items = db.query(ShoppingListItem).filter(
        ShoppingListItem.family_id == family_id
    ).order_by(ShoppingListItem.added_at.desc()).all()
    
    return {
        "id": f"sl-{family_id}",
        "family_id": family_id,
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "quantity": item.quantity,
                "unit": item.unit,
                "checked": item.checked,
                "added_by": item.added_by,
                "added_at": item.added_at.isoformat() if item.added_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None
            }
            for item in items
        ],
        "total_count": len(items),
        "purchased_count": sum(1 for item in items if item.checked),
        "last_updated": datetime.utcnow().isoformat()
    }


@app.post("/shopping-list/item")
def add_shopping_item(
    item: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    family_id = item.get("family_id")
    if not family_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少family_id"
        )
    
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    new_item = ShoppingListItem(
        family_id=family_id,
        name=item.get("name", ""),
        quantity=item.get("quantity", 1.0),
        unit=item.get("unit", "个"),
        checked=item.get("checked", False),
        added_by=current_user.id
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
        "id": new_item.id,
        "name": new_item.name,
        "quantity": new_item.quantity,
        "unit": new_item.unit,
        "checked": new_item.checked,
        "added_by": new_item.added_by,
        "added_at": new_item.added_at.isoformat() if new_item.added_at else None
    }


@app.put("/shopping-list/item/{item_id}")
def update_shopping_item(
    item_id: int,
    updates: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(ShoppingListItem).filter(ShoppingListItem.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="采购项不存在"
        )
    
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == item.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    if "name" in updates:
        item.name = updates["name"]
    if "quantity" in updates:
        item.quantity = updates["quantity"]
    if "unit" in updates:
        item.unit = updates["unit"]
    if "checked" in updates:
        item.checked = updates["checked"]
    item.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(item)
    
    return {
        "id": item.id,
        "name": item.name,
        "quantity": item.quantity,
        "unit": item.unit,
        "checked": item.checked,
        "updated_at": item.updated_at.isoformat() if item.updated_at else None
    }


@app.delete("/shopping-list/item/{item_id}")
def delete_shopping_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(ShoppingListItem).filter(ShoppingListItem.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="采购项不存在"
        )
    
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == item.family_id,
        FamilyMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭的成员"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "删除成功"}


@app.get("/")
def read_root():
    return {"message": "家庭营养管理系统 API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
