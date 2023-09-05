from doit import join_inputs
email = "email"
znak = "znak"
numer = "numer"
umowa = "umowa"
room = "room"

output_string = join_inputs(email, znak, numer, umowa, room)
print("Joined String:", output_string)
