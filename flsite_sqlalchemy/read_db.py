from app import db, Users, Profiles

print(Users.query.all())

res = Users.query.all()
print(res)


print(res[0].email)


f = Users.query.first()

print(f.id)


print(Users.query.filter_by(id = 2).all())
print(Users.query.filter(Users.id == 2).all())


print(Users.query.filter(Users.id > 1).all())


print(Users.query.limit(2).all())

print(Users.query.order_by(Users.email).all())

print(Users.query.order_by(Users.email.desc()).all())


print(Users.query.get(2))


res1 = db.session.query(Users, Profiles).join(Profiles, Users.id == Profiles.user_id).all()
print(res1)

print(res1[0].Users.email)

print(res1[0].Profiles.name)


pr = db.relationship('Profiles', backref='users', uselist=False)

res2 = Users.query.all()
print(res2)

print(res[0].pr)

print(res[0].pr.name)
