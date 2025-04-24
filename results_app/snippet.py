
def checkResult(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['studentid']
            card_pin = form.cleaned_data['cardpin']
            serial = form.cleaned_data['serial']

            try:
                #First check if card exists and it has not been used up to 5 times
                card = TbCard.objects.get(pin=card_pin, serial=serial)
                if card.used == 0:
                    # if the card is valid and not been used up to 5 times
                    # Check if it has been used by the student ID
                    transact = TbTransact.objects.filter(card_serial=card.serial).first()
                    if transact:
                        if transact.student_id == student_id:
                        # If the card has not been used, create a new transaction
                        # and associate it with the student ID
                            fetch_result(request, card.serial, student_id)
                        else:
                            # card has been used by another student ID
                            messages.error(request, "This card has already been used by another student ID.")
                            return render(request, 'results_app/checkresult.html', {'form_key': form})
                            
                    else:
                        fetch_result(request, card.serial, student_id)
                    
                else:
                    return HttpResponse("This card has already been used up to 5 times.")
                
            except TbCard.DoesNotExist:
                return HttpResponse("Invalid card details.")
        else:
            form = ResultForm()
            return render(request, 'results_app/checkresult.html', {'form_key': form})
    else:
        form = ResultForm()
    return render(request, 'results_app/checkresult.html', {'form_key': form})


def fetch_result(request, cardserial, student_id):
    
    # Create a new transaction record
    transact, created = TbTransact.objects.update_or_create(
        serial=cardserial, student_id=student_id, 
        defaults= {'card_use_number' : models.F('card_use_number') + 1} # Increment the use number
        ) 
    if created:
        messages.success(request, "Transaction created successfully.")
    else:
        messages.info(request, "Transaction updated successfully. {card_use_number} times used.")
    try:
        result = TbResults.objects.get(student_id=student_id)
        result_dict = {
            'student_id': result.student_id,
            'student_name': result.student_name,
            'Maths': result.Maths,
            'English': result.English,
            'Economics': result.Economics,
            'Biology': result.Biology,
            'Total': result.Total,  # Assuming these are @property fields
            'Avscore': result.Avscore,
            'Grade': result.Grade
        }
        context = {
            'form_key': result_dict,
            'use_key' : transact.card_use_number
        }
        return render(request, 'results/checkresult.html', context)
    except TbResults.DoesNotExist:
        messages.error(request, "Student result not found")
        return render(request, 'results/checkresult.html', {'form_key': ResultForm(request.POST)})
    
    
def checkResult(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['studentid']
            card_pin = form.cleaned_data['cardpin']
            serial = form.cleaned_data['serial']

            try:
                #First check if card exists and it has not been used up to 5 times
                card = TbCard.objects.get(pin=card_pin, serial=serial)
                if card.used == 0:
                    # if the card is valid and not been used up to 5 times
                    # Check if it has been used by the student ID
                    transact = TbTransact.objects.filter(card_serial=card.serial).first()
                    if transact:
                        if transact.student_id == student_id:
                        # If the card has not been used, create a new transaction
                        # and associate it with the student ID
                            fetch_result(request, card.serial, student_id)
                        else:
                            # card has been used by another student ID
                            messages.error(request, "This card has already been used by another student ID.")
                            return render(request, 'results_app/checkresult.html', {'form_key': form})
                            
                    else:
                        fetch_result(request, card.serial, student_id)
                    
                else:
                    return HttpResponse("This card has already been used up to 5 times.")
                
            except TbCard.DoesNotExist:
                return HttpResponse("Invalid card details.")
        else:
            form = ResultForm()
            return render(request, 'results_app/checkresult.html', {'form_key': form})
    else:
        form = ResultForm()
    return render(request, 'results_app/checkresult.html', {'form_key': form})


def fetch_result(request, cardserial, student_id):
    
    # Create a new transaction record
    transact, created = TbTransact.objects.update_or_create(
        serial=cardserial, student_id=student_id, 
        defaults= {'card_use_number' : models.F('card_use_number') + 1} # Increment the use number
        ) 
    if created:
        messages.success(request, "Transaction created successfully.")
    else:
        messages.info(request, "Transaction updated successfully. {card_use_number} times used.")
    try:
        result = TbResults.objects.get(student_id=student_id)
        result_dict = {
            'student_id': result.student_id,
            'student_name': result.student_name,
            'Maths': result.Maths,
            'English': result.English,
            'Economics': result.Economics,
            'Biology': result.Biology,
            'Total': result.Total,  # Assuming these are @property fields
            'Avscore': result.Avscore,
            'Grade': result.Grade
        }
        context = {
            'form_key': result_dict,
            'use_key' : transact.card_use_number
        }
        return render(request, 'results/checkresult.html', context)
    except TbResults.DoesNotExist:
        messages.error(request, "Student result not found")
        return render(request, 'results/checkresult.html', {'form_key': ResultForm(request.POST)})    


def fetch_result(request, serial, student_id):
    # Create or update transaction record
    transact, created = TbTransact.objects.update_or_create(
        serial=serial,
        student_id=student_id,
        defaults={'card_use_number': models.F('card_use_number') + 1}
    )
    
    try:
        result = TbResults.objects.get(student_id=student_id)
        result_dict = {
            'student_id': result.student_id,
            'student_name': result.student_name,
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
            'use_key': transact.card_use_number  # Use the actual field from transaction
        }
        
        messages.success(request, f"Result retrieved. Card used {transact.card_use_number} times.")
        return render(request, 'results_app/checkresult.html', context)
        
    except TbResults.DoesNotExist:
        messages.error(request, "Student result not found")
        return render(request, 'results_app/checkresult.html', {'form_key': ResultForm(request.POST)})
    
    def signupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # Redirect to a success page or home page
    else:
        form = UserCreationForm()
    return render(request, 'users_app/signup.html', {'form': form})

# When using Django's built-in UserCreationForm, you can customize the form to include additional fields if needed.
    # For example, you can create a custom form that inherits from UserCreationForm and add fields like email, first name, etc.
    # However, for simplicity, we will use the default UserCreationForm here.
    # If you want to customize the form, you can do it like this:
    # from django import forms
    # from django.contrib.auth.models import User
    # from django.contrib.auth.forms import UserCreationForm
    # class CustomUserCreationForm(UserCreationForm):
    #     email = forms.EmailField(required=True)
    #     class Meta:
    #         model = User
    #         fields = ('username', 'email', 'password1', 'password2')
    #     def save(self, commit=True):
    #         user = super().save(commit=False)
    #         user.email = self.cleaned_data['email']
    #         if commit:
    #             user.save()
    #         return user
    # Then, in your view, you can use CustomUserCreationForm instead of UserCreationForm.
    
    # when using the built-in logout view, a href doesnt work in template cos it must be
    # a post request so use a csrf form and use css to make the button look like a link e.g.
    # <button type="submit" style="background: none; border: none; cursor: pointer; 
    # color: blue; text-decoration: underline; padding: 0;">
    