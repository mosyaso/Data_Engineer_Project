###### Without OOP ####
# programmer = 'Vina'
# petani = 'Wahyuni'
# doktor = 'Eka'

# def programmer_makan():
#     print('{} makan nasi'.format(programmer))

# def petani_makan():
#     print('{} makan nasi'.format(petani))

# def doktor_makan():
#     print('{} makan nasi'.format(doktor))

# programmer_makan()
# petani_makan()
# doktor_makan()

##### Class and Object #####
class Manusia(object):
    nama = None #attribute

    def __init__(self, nama): #base class
        self.nama = nama

    def makan(self):
        print('{} makan nasi'.format(self.nama))

# programmer = Manusia('Vina')
# programmer.makan()

# petani = Manusia('Wahyuni')
# petani.makan()

# doctor = Manusia('Eka')
# doctor.makan()

##### Inheritance #####
class ManusiaMilenial(Manusia):
    email = None
    __password = None #private

    def set_email(self, email):
        self.email = email
    
    def set_pass(self, password):
        self.__password = password
    
    def __samarkan_password(self):
        return self.__password.replace('a', '*')
    
    def info(self): #Encapsulation
        print('nama={}, email={}, pass={}'.format(self.nama, self.email, self.__samarkan_password()))
        #print('nama={}, email={}'.format(self.nama, self.email))
        #print('nama={}, email={}, pass{}'.format(self.nama, self.email, self.password))
    
# programmer = ManusiaMilenial('Vina')
# programmer.set_email('vina@test.com')
# programmer.info()

# petani = ManusiaMilenial('Wahyuni')
# petani.set_email('wahyuni@test.com')
# petani.info()

# doctor = ManusiaMilenial('Eka')
# doctor.set_email('eka@test.com')
# doctor.info()

##### Encapsulation #####
# programmer = ManusiaMilenial('Vina')
# programmer.set_email('vina@test.com')
# programmer.set_pass('rahsia')
# programmer.info()

##### Polymorphism #####
class Programmer(ManusiaMilenial):
    
    def info(self): #Polymorphism
        print('nama={}/email={}'.format(self.nama, self.email))

class Influencer(ManusiaMilenial):
    
    def info(self): #Encapsulation
        print('nama={}, email={}'.format(self.nama, self.email))

programmer = Programmer('Vina')
programmer.set_email('vina@test.com')
programmer.set_pass('rahsia')
programmer.info()

influencer = Influencer('Wahyuni')
influencer.set_email('Wahyuni@test.com')
influencer.set_pass('abc123')
influencer.info()