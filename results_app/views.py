from django.shortcuts import render
from django.http import HttpResponse
from .models import TbResults, TbCard, TbTransact
from .forms import ContactForm, ResultForm, LoginForm, SignUpForm, CardForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.db import models # so that models.F would work
import random

# Create your views here.
def index (request):
    context = {
        'title': 'Results App',
        'heading': 'Welcome to the Results App',
        'description': 'This app allows you to manage and view student results.',
        'datas': 'This is a remake of my results app with Django ORM throughout'
    }
    return render (request, 'results_app/index.html', context )

def get_all_results(request):
    all_results = TbResults.objects.all()
    context = {
        'title': 'All Results',
        'heading': 'All Student Results',
        'data': all_results,
    }
    return render(request, "results_app/allresults.html", context= {'data': all_results})

def hash_pin(pin):
    # Placeholder for hashing function
    return pin  # Replace with actual hashing logic

def checkResult(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['studentid']
            card_pin = form.cleaned_data['cardpin']
            serial = form.cleaned_data['serial'] 
            strpin = str(card_pin) #.zfill(12) add in production
            
            try:
                card = TbCard.objects.get(serial=serial, is_valid=True)
                if not check_password(strpin, card.pin):
                    messages.error(request, "Invalid card PIN.")
                    return render(request, 'results_app/checkresult.html', {'form_key': form})
                
            except TbCard.DoesNotExist:
                messages.error(request, "Invalid card details.")
                return render(request, 'results_app/checkresult.html', {'form_key': form})
            if card.student_id and card.student_id != student_id:
                messages.error(request, "This card has already been used by another student ID.")
                return render(request, 'results_app/checkresult.html', {'form_key': form})
            
            if not card.student_id:
                card.student_id = student_id
                
            card.usage_count += 1    
            if card.usage_count >= 6:
                card.is_valid = False
                card.save()
                messages.error(request, "This card has already been used up to 5 times.")
                return render(request, 'results_app/checkresult.html', {'form_key': form})
            card.save()
            #fetch_result(request, student_id, usage_count=card.usage_count)
            try:
        
                result = TbResults.objects.get(student_id=student_id)
                result_dict = {
                    'student_name': result.student_name,
                    'student_id': result.student_id,
                    'Maths': result.Maths,
                    'English': result.English,
                    'Economics': result.Economics,
                    'Biology': result.Biology,
                    'Total': result.Total,
                    'Avscore': result.Avscore,
                    'Grade': result.Grade
                }
                context = {
                    'form_key': result_dict,
                    'use_key' : card.usage_count
                }
                return render(request, 'results_app/displayresult.html', context)
            except TbResults.DoesNotExist:
                messages.error(request, "Student result not found")
                return render(request, 'results_app/checkresult.html', {'form_key': ResultForm(request.POST)})
            
        else:
            form = ResultForm()
        return render(request, 'results_app/checkresult.html', {'form_key': form})        
    else:
        form = ResultForm()
        return render(request, 'results_app/checkresult.html', {'form_key': form})        

def fetch_result(request, student_id, usage_count):
    try:
        
        result = TbResults.objects.get(student_id=student_id)
        result_dict = {
            'student_name': result.student_name,
            'student_id': result.student_id,
            'maths': result.Maths,
            'english': result.English,
            'economics': result.Economics,
            'biology': result.Biology,
            'total': result.Total,
            'average_score': result.Avscore,
            'grade': result.Grade
        }
        context = {
            'form_key': result_dict,
            'use_key' : usage_count
        }
        return render(request, 'results_app/displayresult.html', context)
    except TbResults.DoesNotExist:
        messages.error(request, "Student result not found")
        return render(request, 'results_app/checkresult.html', {'form_key': ResultForm(request.POST)})
    
@login_required
def makeCard(request):
    # Placeholder for card creation logic
    if request.method  == 'POST':
        form = CardForm(request.POST)
        print(form.data)
        if form.is_valid():
            print("Form is valid")
            number_of_cards = form.cleaned_data['number_of_card']
            createCards(number_of_cards)
            print(f"{number_of_cards} cards created successfully.")
            messages.success(request, f"{number_of_cards} cards created successfully.")
            return render(request, 'results_app/makecard.html', {'form_key': form})
        else:
            print("Form is not valid")
            print(f"Form errors: {form.errors}")
            form = CardForm()    
            return render(request, 'results_app/makecard.html', {'form_key': form})    
    else:
        print("GET request")
        form = CardForm()    
        return render(request, 'results_app/makecard.html', {'form_key': form})
    
def createCards(number_of_cards):   
    # create a card with a random pin and serial number
    # hash it and save it to the database 
    for _ in range(1, number_of_cards):
        pin = random.randint(000_000_000_000, 999_999_999_999)
        serial = random.randint(100000, 999999)
        pin = str(pin).zfill(12)
        print (f"Creating card with PIN: {pin} and Serial: {serial}")
        # Hash pin before saving
        TbCard.objects.create(pin=make_password(pin), serial=serial, is_valid=True)
        print(f"Card with PIN: {pin} and Serial: {serial} created.")
        # Format the pin and serial for display
        printpin = pin[0:4] +'-' + pin[4:8] + '-' + pin[8:12]
        serial = str(serial)
        printserial = serial[0:3] + ' ' + serial[3:6]
        
        # Save the card details to a file
        with open('card.txt', 'a') as f:
            f.write(f"Card with PIN: {printpin} and Serial: {printserial} created.\n")
    return HttpResponse(f"{number_of_cards} cards created successfully.")