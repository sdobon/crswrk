import updatewumpus

name = updatewumpus.intialize_world()

print updatewumpus.take_action(name, "Up")
print updatewumpus.look_ahead(name)
print updatewumpus.take_action(name, "Step")
print updatewumpus.take_action(name, "Right")
print updatewumpus.take_action(name, "Step")
print updatewumpus.look_ahead(name)
print updatewumpus.take_action(name, "Up")
print updatewumpus.look_ahead(name)

updatewumpus.take_action(name, "Exit")
