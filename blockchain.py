import datetime
import hashlib
import random


class Transaction:
    id = 0
    sender = None  # Adresse qui envoie
    receiver = None  # Adresse qui reçoit
    value = 0  # Valeur de la transaction
    fee = 0  # Frais de la transaction

    # Création d'une transaction aléatoire lors de l'initialisation d'une transaction
    def __init__(self, id):
        self.id = id
        self.value = float(random.randint(1, 2_000))
        self.fee = self.value * 0.00002
        self.sender = hashlib.sha256(str(random.randint(0, 256_000_000)).encode('utf-8')).hexdigest()
        self.receiver = hashlib.sha256(str(random.randint(0, 256_000_000)).encode('utf-8')).hexdigest()

    # Fonction qui hashe (SHA-256) les données de la transaction
    def hash_transac(self):
        data = hashlib.sha256()
        data.update(
            str(self.sender).encode('utf-8') +
            str(self.receiver).encode('utf-8') +
            str(self.value).encode('utf-8') +
            str(self.fee).encode('utf-8')
        )
        return data.hexdigest()

    # Affichage des données de la transaction lorsqu'on le print
    def __str__(self):
        return "\n----- Transaction N°" + str(self.id) + " -----" \
               + "\nId : " + str(self.id) \
               + "\nAdresse d'entrée : " + str(self.sender) \
               + "\nAdresse de sortie : " + str(self.receiver) \
               + "\nValeur de la transaction : " + str(self.value) + " BTC" \
               + "\nFrais de transaction : " + str(self.fee)


class Block:
    id = None
    root_hash = ''  # Hash des données du block
    leaves = None  # Liste/tableau des leaves, voir Block.create_leaves()
    transactions = None  # Liste/tableau des transactions (hashé)
    timestamp = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f")  # Date de la création du Block
    prev_hash = None  # Hash du block précédent
    next = None  # Voir Blockchain.add_block()

    def __init__(self, id):
        self.id = id
        self.leaves = []
        self.transactions = []

    # Création des leaves
    # Une leaf correspond à un hash d'une paire de transactions déjà hashées
    # S'adapte si le nombres de toutes les transactions sont pairs ou impairs
    def create_leaves(self):
        length = len(self.transactions)
        cmt = 0
        while cmt < length:
            if length - cmt >= 2:  # On hashe chaque paire de transactions
                hashed_data = hashlib.sha256()
                hashed_data.update(
                    str(self.transactions[cmt]).encode('utf-8') +
                    str(self.transactions[cmt + 1]).encode('utf-8')
                )
                self.leaves.append(hashed_data.hexdigest())
            else:  # Si il reste une dernière transaction...
                hashed_data = hashlib.sha256()
                hashed_data.update(
                    str(self.transactions[cmt]).encode('utf-8')
                )
                self.leaves.append(hashed_data.hexdigest())
            cmt += 2

    # Fonction qui concatène et hashe tous les leaves du block + la date de création du block + le hash précédent
    # Le résultat de cette fonction donne le root hash du block
    def create_root_hash(self):
        length = len(self.leaves)
        data = ''
        for n in range(length):
            data += str(self.leaves[n])
        hashed_data = hashlib.sha256()
        hashed_data.update(
            data.encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.prev_hash).encode('utf-8')
        )
        self.root_hash = hashed_data.hexdigest()

    # Affichage des données du block lorsqu'on le print
    def __str__(self):
        return "\n----- Block " + str(self.id) + " -----" \
               + "\nRoot hash : " + str(self.root_hash) + '\n' \
               + "\nDate de création : " + str(self.timestamp) \
               + "\nNombre de transactions : " + str(len(self.transactions)) \
               + "\nHash du block précédent : " + str(self.prev_hash)


class Blockchain:
    block = Block(0)  # Création du block 0 lors de l'initialisation de la blockchain

    def __init__(self):
        self.fill_block()  # Voir Blockchain.fill_block()

    # Ajout d'un block à la blockchain
    def add_block(self, block):
        block.prev_hash = self.block.root_hash  # On ajoute le hash du précédent block au nouveau

        self.block.next = block
        self.block = self.block.next
        self.fill_block()

    # Fonction qui va créer les transactions + les leaves + le root hash pour chaque block
    def fill_block(self):
        for n in range(7):
            transac = Transaction(n + 1)
            self.block.transactions.append(transac.hash_transac())
        self.block.create_leaves()
        self.block.create_root_hash()
        print(self.block)


# # # # # Début du script # # # # #

print("\n---------- Création d'une blockchain ----------\n")

# On demande à l'utilisateur combien de block il veut créer
nbBlocks = int(input("- Combien de blocks voulez vous créer ? : "))

# On initialise la blockchain puis on ajoute les blocks
blockchain = Blockchain()
for n in range(nbBlocks):
    blockchain.add_block(Block(n + 1))
