import ipfsapi
import os

ipfs = ipfsapi.connect('47.98.122.3', '5001')

current_path = os.getcwd()

print(current_path)

medias_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

real_medias_path = os.path.join(medias_path, 'medias')

print(real_medias_path)

parents = os.listdir(real_medias_path)

for file in parents:
    filepath = os.path.join(real_medias_path,file)
    res = ipfs.add(filepath)
    print(res)


