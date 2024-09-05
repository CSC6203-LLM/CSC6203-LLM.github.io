from llmzoo import Model

model = Model("phoenix",ip="http://61.241.103.32")
print(model.response("how are you"))