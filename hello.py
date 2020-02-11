from flask import Flask, flash, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
import random
import pickle
from random import randint
#imported libraries 

#@app.route('/files/<fname>') 
#def page_file_view(fname): 
#    fullname = os.path.join(as_user.get_user_folder(mod_cfg, get_user()),fname)
#     with open(fullname, 'rb') as f: 
#        txt = f.read() 
#    return 'viewing file ' + fname + ' first line = ' + str(txt)

UPLOAD_FOLDER = '/Users/egortrofimov/Documents/Project/flask/static/img'
ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']


hello = Flask(__name__) 
hello.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
hello.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#lines needed to launch the Flask project

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

hello.config['MAIL_SERVER'] = ''
hello.config['MAIL_PORT'] = 465
hello.config['MAIL_USE_SSL'] = True


MAIL_USERNAME = ''
MAIL_PASSWORD = ''

#hello.config.from_pyfile('config.cfg')

mail = Mail(hello)
#EMail sender activated above 

dog_walkers = []
dog_owners = []
#two imortant lists of all users that are registered in the system

#############################################################################################################################
#This function is made to upload the persons data from pickle file every time a program starts

def uploadPerson():
 
    global dog_owners 
    global dog_walkers

    outfile = open('dogWalkers.txt','rb')
    dog_walkers = dog_walkers + (pickle.load(outfile))
    outfile.close() 

    outfile = open('dogOwners.txt','rb')
    dog_owners = dog_owners + (pickle.load(outfile))
    outfile.close() 

############################################################################################################################
#Class defenitions that are required to save the data from the website forms 
class Address:

#class that works with address data from the web-site

    def __init__(self, house_num, street, city, post_code):
        self.house_num = house_num
        self.street = street
        self.city = city
        self.post_code = post_code

    def __str__(self):
        return self.house_num + ", " + self.street + ", " + self.city + ", " + self.post_code


class Dog:

#dog class that is used when a dog-owner creates a dog to add to the his dog list
   
    def __init__(self, name, dogtype, size):
        self.name = name
        self.type = dogtype
        self.size = size
    
    def setDogImage(self,dog_image):
        self.dog_image = dog_image

    def __str__(self):
        return "Dogs name: " + self.name + ",  " + "Dogs type: " + self.type +  ",  " + "Dogs size: " + self.size


class Person():

#main class which plays a massive roll in the dataflow of the system
#all data that is entered in the website is saved via this class

    description = ""

    def generateID(self):
        key = []
        k=[]
        dict_types = ["name","surname", "email", "tel_num", "password"]

        for letter in range (0,12):
            dict_type = random.choice(dict_types)
            list_type = [self.__dict__[dict_type]]
            k.append(list_type[0][random.randint(0,int(len(list_type[0])-1))])
        key = "".join(k)  
        return key            
    
    def createAddress(self, house_num, street, city, post_code):
        newAddress = Address(house_num, street, city, post_code)
        return newAddress
    
    def __init__(self, name, surname, email, city, house_num, street, post_code, tel_num, password):
        
        self.name = name
        self.surname = surname
        self.email = email
        self.address = self.createAddress(house_num, street, city, post_code)
        self.tel_num = tel_num
        self.password = password
        self.id = self.generateID()
    
    def addDescriptionANDImage(self,desc,ima):
        self.description = desc
        self.image = ima
    

class Dog_Walker(Person):

#sub class of a dog walker, it is exacly the same as the Person class

    def __init__(self, name, surname, email, city, house_num, street, post_code, tel_num, password):
        Person.__init__(self, name, surname, email, city, house_num, street, post_code, tel_num, password)
        self.rating = "5"
    

class Dog_Owner(Person):

#sub class of dog owner, both is used to represent dogs and a person data

    dogs = []

    def createDoggy(self,d_n,d_t,d_s):
        newDog = Dog(d_n,d_t,d_s)
        self.dogs.append(newDog)
        return newDog

    def __init__(self, name, surname, email, city, house_num, street, post_code, dog_name, dog_type, dog_size,tel_num, password):
        Person.__init__(self, name, surname, email, city, house_num, street, post_code, tel_num, password)
        #the dog is a list of dog of class dog
        self.dogs = self.createDoggy(dog_name,dog_type,dog_size)
        print(self.dogs)

##############################################################################################################################
#This code here takes back all the information from text files, so there is the info about all users

uploadPerson()

############################################################################################################################
#Actual program that launches the web-site 
@hello.route('/')
def index():
    try:
            return render_template("who_are_you.html", **locals())
    except Exception as e:
            return str(e)

@hello.route("/register.html", methods=["GET", "POST"] )
def register(): 
    return render_template("register.html")

@hello.route('/more_info.html', methods=["GET", "POST"])
def more_info():
    
    # Read all the info from the form
    # Create a new object and pass the info

    name = request.form.get("selectName")
    surname = request.form.get("selectSurname")
    email = request.form.get("selectEmail")
    tel_num = request.form.get("selectTel_Num")
    street = request.form.get("selectStr")
    city = request.form.get("selectCity")
    house_num = request.form.get("selectHouseNumber")
    post_code = request.form.get("selectPost_Code")
    pswrd1 = request.form.get("selectPsswrd1")
    pswrd2 = request.form.get("selectPsswrd2")
     
    nw = Dog_Walker(name,surname,email, city, house_num, street, post_code,tel_num,pswrd1) 
    dog_walkers.append(nw)

    currentID = nw.id
    
    print(currentID)

    session['currentID'] = currentID
    #filling uo the file with the registrated information
    outfile = open('dogWalkers.txt','wb')

    pickle.dump(dog_walkers, outfile)
    outfile.close() 

    return render_template('more_info.html', **locals())
  
@hello.route('/register_dog.html', methods=["GET", "POST"])
def register_dog():
    return render_template("register_dog.html", **locals())
    
@hello.route('/sign_in.html', methods=["GET", "POST"])
def sign_in():
    return render_template("sign_in.html")

@hello.route('/are_you_a.html', methods=["GET","POST"])
def are_you_a():

    confEmail = request.form.get("confirmEmail")
    confPassword = request.form.get("confirmPassword")

    for walker in dog_walkers:
        if walker.email == confEmail:
            if walker.password == confPassword:
                name = walker.name
                surname = walker.surname
                email = walker.email
                address = walker.address
                tel_num = walker.tel_num
                description = walker.description
                image = walker.image


                num = randint(0,len(dog_owners)-1)
                nm = dog_owners[num].name
                srnm = dog_owners[num].surname
                ml = dog_owners[num].email
                ddrss = dog_owners[num].address
                tl_nm = dog_owners[num].tel_num
                dscrptn = dog_owners[num].description
                img = dog_owners[num].image
                
                return render_template("main_page_walker_view.html", **locals())
        else:
            for owner in dog_owners:
                if owner.email == confEmail:
                    if owner.password == confPassword:
                        name = owner.name
                        surname = owner.surname
                        email = owner.email
                        address = owner.address
                        tel_num = owner.tel_num
                        description = owner.description
                        image = owner.image
                        dog_details = owner.dogs
                        dimage = owner.dogs.dog_image
                        return render_template("main_page_owner_view.html", **locals())
    
            
    return render_template("sign_in.html")
        
            
            
@hello.route('/main_page_walker_view.html', methods=["GET", "POST"])
def main_page_walker_view():
    currentID = session.get('currentID')
    user_info = request.form.get("infoAboutUser")
    users_picture = request.form.get("userPic")

    print(user_info,users_picture)
   
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'userPic' not in request.files:
            
            flash('No file part')
            return redirect(request.url)
        file = request.files['userPic']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(hello.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
 
    #that loop adds the description and image to ower dog_walker class 
    #in this loop we get all data from out users, that way we can place it on our web-page

    print(user_info,users_picture)

    for walker in dog_walkers:
        if walker.id == currentID:
            
            walker.addDescriptionANDImage(user_info,users_picture)

            outfile = open('dogWalkers.txt','wb')
            pickle.dump(dog_walkers, outfile)
            outfile.close()

            name = walker.name
            surname = walker.surname
            email = walker.email
            address = walker.address
            tel_num = walker.tel_num
            description = walker.description
            image = walker.image
            print("passed")
        else:
            pass

    num = randint(0,len(dog_owners)-1)
    nm = dog_owners[num].name
    srnm = dog_owners[num].surname
    ml = dog_owners[num].email
    ddrss = dog_owners[num].address
    tl_nm = dog_owners[num].tel_num
    dscrptn = dog_owners[num].description
    img = dog_owners[num].image

    return render_template("main_page_walker_view.html", **locals())


@hello.route('/more_info_dog.html', methods=["GET", "POST"])
def more_info_dog():
    # Read all the info from the form
    # Create a new object and pass the info

    Name = request.form.get("SelectName")
    Surname = request.form.get("SelectSurname")
    Email = request.form.get("SelectEmail")
    Tel_num = request.form.get("SelectTel_Num")
    House_Num = request.form.get("SelectHouseNumber")
    Street = request.form.get("SelectStr")
    City = request.form.get("SelectCity")
    PostCode = request.form.get("SelectPostCode")
    DogName = request.form.get("SelectDogName")
    DogType = request.form.get("SelectDogType")
    DogSize = request.form.get("SelectDogSize")
    Pswrd1 = request.form.get("SelectPsswrd1")
    Pswrd2 = request.form.get("SelectPsswrd2")
     
    no = Dog_Owner(Name,Surname,Email,City,House_Num, Street, PostCode,DogName,DogType,DogSize,Tel_num,Pswrd1) 
    dog_owners.append(no)

    CurrentID = no.id

    session['CurrentID'] = CurrentID
    
    outfile = open('dogOwners.txt','wb')

    pickle.dump(dog_owners, outfile)
    outfile.close()

    return render_template("more_info_dog.html", **locals())
   
    

@hello.route('/main_page_owner_view.html', methods=["GET", "POST"])
def main_page_owner_view():
    
    CurrentID = session.get('CurrentID')
    User_Info = request.form.get("InfoAboutUser")
    User_Picture = request.form.get("ProfilePic")
    Dog_Picture = request.form.get("DogPic")

    for owner in dog_owners:
        if owner.id == CurrentID:
            owner.addDescriptionANDImage(User_Info,User_Picture)
            owner.dogs.setDogImage(Dog_Picture)

            outfile = open('dogOwners.txt','wb')
            pickle.dump(dog_owners, outfile)
            outfile.close()

            name = owner.name
            surname = owner.surname
            email = owner.email
            address = owner.address
            tel_num = owner.tel_num
            description = owner.description
            image = owner.image
            dog_details = owner.dogs
            dimage = owner.dogs.dog_image
            print("passed")
        else:
            pass


    return render_template("main_page_owner_view.html", **locals())


@hello.route('/final_page.html')
def final_page():
    msg = Message('Hello', sender='', recipients=[''])
    mail.send(msg)
    return render_template("final_page.html")

if __name__ == "__main__":
    hello.run(debug=True)   