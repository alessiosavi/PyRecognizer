"""
Generate the administrator of the neural network, delegated to train/tune the model
"""
import sys
sys.path.insert(0, "../")

from datastructure.Administrator import Administrator

# Creating a new administrator with the following credentials
a = Administrator("name", "mail", "password")
a.init_redis_connection()
print("Remove user -> {}".format(a.remove_user()))
print("Add user -> {}".format(a.add_user()))
print("Verify login {}".format(a.verify_login("password")))
