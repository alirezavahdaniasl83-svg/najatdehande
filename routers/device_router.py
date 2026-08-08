from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from device_service import register_device, get_devices


router = APIRouter(
    prefix="/api/devices",
    tags=["devices"]
)


class DeviceRegistration(BaseModel):
    device_id: str
    name: str | None = None
    model: str | None = None
    android_version: str | None = None
    battery: int | None = None


@router.post("/register")
async def register(device: DeviceRegistration):

    if not device.device_id.strip():
        raise HTTPException(
            status_code=400,
            detail="device_id is required"
        )

    if device.battery is not None:
        if device.battery < 0 or device.battery > 100:
            raise HTTPException(
                status_code=400,
                detail="battery must be between 0 and 100"
            )

    register_device(
        device_id=device.device_id,
        name=device.name,
        model=device.model,
        android_version=device.android_version,
        battery=device.battery,
    )

    return {
        "success": True,
        "message": "Device registered successfully",
        "device_id": device.device_id
    }


@router.get("/")
async def devices():

    return {
        "success": True,
        "devices": get_devices()
    }
