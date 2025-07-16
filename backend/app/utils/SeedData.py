def seed_data():
    from app import db
    from app.models.enums.UserRole import UserRole
    from app.models.enums.AccountStatus import AccountStatus
    from app.models.enums.SensorStatus import SensorStatus
    from app.models.enums.FanStatus import FanStatus
    from app.utils.PasswordUtils import hash_password
    import random
    from datetime import datetime, timezone

    from app.models.User import User
    from app.models.Account import Account
    from app.models.Command import Command
    from app.models.Fan import Fan
    from app.models.Alert import Alert
    from app.models.Reading import Reading
    from app.models.Sensor import Sensor
    from app.models.Zone import Zone
    
    if User.query.first():
        return
    
    if db.session.query(User).first():
        return
    
    admin_user = User(
        username="admin",
        password=hash_password("11111111")
    )
    admin_account = Account(
        full_name="Admin",
        email="admin@airwatch.com",
        role=UserRole.ADMIN,
        status=AccountStatus.ACTIVE,
        user=admin_user
    )
    db.session.add(admin_user)
    
    # Sensores
    sensors = [
        Sensor(serial_number=f"SENSOR-{i+1}", purchase_date=datetime.now(timezone.utc)) for i in range(5)
    ]
    db.session.add_all(sensors)
    
    # Ventiladores
    fans = [
        Fan(serial_number=f"FAN-{i+1}", purchase_date=datetime.now(timezone.utc)) for i in range(5)
    ]
    db.session.add_all(fans)
    
    db.session.flush()
    
    # Zonas
    locations = ["144px 177px", "129px 412px", "265px 514px"]
    shuffled_sensors = random.sample(sensors, len(locations))
    shuffled_fans = random.sample(fans, len(locations))
    
    for i in range(len(locations)):
        shuffled_sensors[i].status = SensorStatus.ACTIVE.value
        
        zone = Zone(
            name=f"Zona {i+1}",
            location=locations[i],
            area=random.uniform(20.0, 100.0),
            sensor=shuffled_sensors[i],
            fan=shuffled_fans[i]
        )
        db.session.add(zone)
    
    db.session.commit()
