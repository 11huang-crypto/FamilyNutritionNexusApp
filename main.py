from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Union
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "family-nutrition-nexus-secret-key-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./family-nutrition.db")

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
    created_at = Column(DateTime, default=datetime.utcnow)


class Family(Base):
    __tablename__ = "families"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    admin = relationship("User", back_populates="families")


class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)


class HealthProfile(Base):
    __tablename__ = "health_profiles"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    conditions = Column(Text)
    allergens = Column(Text)
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


class HealthProfileResponse(BaseModel):
    id: int
    family_id: int
    user_id: int
    name: str
    conditions: List[str]
    allergens: List[str]

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
        user_id=current_user.id,
        name=profile.name,
        conditions=str(profile.conditions),
        allergens=str(profile.allergens)
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return HealthProfileResponse(
        id=new_profile.id,
        family_id=new_profile.family_id,
        user_id=new_profile.user_id,
        name=new_profile.name,
        conditions=eval(new_profile.conditions),
        allergens=eval(new_profile.allergens)
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
            "conditions": eval(p.conditions),
            "allergens": eval(p.allergens),
            "created_at": p.created_at,
            "updated_at": p.updated_at
        })
    
    return {"profiles": result}


@app.put("/health/profile/{profile_id}")
def update_health_profile(
    profile_id: int,
    profile: HealthProfileCreate,
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
    
    existing_profile.name = profile.name if profile.name else existing_profile.name
    existing_profile.conditions = str(profile.conditions) if profile.conditions else existing_profile.conditions
    existing_profile.allergens = str(profile.allergens) if profile.allergens else existing_profile.allergens
    existing_profile.updated_at = datetime.now(datetime.timezone.utc)
    
    db.commit()
    db.refresh(existing_profile)
    
    return {"message": "健康档案更新成功"}


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


@app.get("/")
def read_root():
    return {"message": "家庭营养管理系统 API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
