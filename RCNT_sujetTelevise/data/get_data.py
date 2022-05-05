# # # # # # # # # # # # # # # # # # # # # # # # # #
# Nos deux bases de données proviennent de l INA  #
# # # # # # # # # # # # # # # # # # # # # # # # # #

url_nb = "https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114045/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv"
url_time =  "https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114231/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-durees.csv"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Nous pouvons directement les télécharger sous format .csv   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # #
# Probleme dans le format du csv. On retire les ';' en trop...     #
# # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # #
input_file =


# Open the file as read
f = open(input_file, "r+")
# Create an array to hold write data
new_file = []
# Loop the file line by line
for line in f:
    new_line = line[:-2]
    new_file.append(new_line)

with open(input_file, "w+") as f:
    for i in new_file:
        f.write(i + "\n")

