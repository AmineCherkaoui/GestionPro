# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import password_validation


class UserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirmer le mot de passe")
    ALL_ADD = forms.BooleanField(required=False, label="Create")
    ALL_CHANGE = forms.BooleanField(required=False, label="Update")
    ALL_DELETE = forms.BooleanField(required=False, label="Delete")

    class Meta:
        model = User
        fields = ['username', "email", "is_superuser"]



    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            self.assign_permissions(user)

        return user

    def assign_permissions(self, user):
        if self.cleaned_data.get('ALL_ADD'):
            add_group, _ = Group.objects.get_or_create(name='Create')
            add_perms = Permission.objects.filter(codename__startswith='add_')
            add_group.permissions.set(add_perms)
            user.groups.add(add_group)

        if self.cleaned_data.get('ALL_CHANGE'):
            change_group, _ = Group.objects.get_or_create(name='Update')
            change_perms = Permission.objects.filter(codename__startswith='change_')
            change_group.permissions.set(change_perms)
            user.groups.add(change_group)

        if self.cleaned_data.get('ALL_DELETE'):
            delete_group, _ = Group.objects.get_or_create(name='Delete')
            delete_perms = Permission.objects.filter(codename__startswith='delete_')
            delete_group.permissions.set(delete_perms)
            user.groups.add(delete_group)


class UserEditForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label="Changer le mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirmer le mot de passe")
    ALL_ADD = forms.BooleanField(required=False, label="Create")
    ALL_CHANGE = forms.BooleanField(required=False, label="Update")
    ALL_DELETE = forms.BooleanField(required=False, label="Delete")

    class Meta:
        model = User
        fields = ['username', 'email', 'is_superuser']
        labels={
            "username":"Nom d'utilisateur",
            "email":"Adresse e-mail",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['ALL_ADD'].initial = self.instance.groups.filter(name='Create').exists()
            self.fields['ALL_CHANGE'].initial = self.instance.groups.filter(name='Update').exists()
            self.fields['ALL_DELETE'].initial = self.instance.groups.filter(name='Delete').exists()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 or password2:
            if not password1:
                self.add_error('password1', "Please enter a new password.")
            if not password2:
                self.add_error('password2', "Please confirm your new password.")
            if password1 and password2 and password1 != password2:
                self.add_error('password2', "The passwords don't match.")

            try:
                password_validation.validate_password(password1)
            except forms.ValidationError as e:
                for error in e.messages:
                    self.add_error('password2', error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)

        if commit:
            user.save()
            self.remove_existing_permissions(user)
            self.assign_permissions(user)

        return user

    def remove_existing_permissions(self, user):
        """Remove existing permissions from the user before reassigning."""
        add_group = Group.objects.get(name='Create')
        change_group = Group.objects.get(name='Update')
        delete_group = Group.objects.get(name='Delete')

        user.groups.remove(add_group)
        user.groups.remove(change_group)
        user.groups.remove(delete_group)

    def assign_permissions(self, user):
        """Assign new permissions to the user based on form input."""
        if self.cleaned_data.get('ALL_ADD'):
            add_group, _ = Group.objects.get_or_create(name='Create')
            add_perms = Permission.objects.filter(codename__startswith='add_')
            add_group.permissions.set(add_perms)
            user.groups.add(add_group)

        if self.cleaned_data.get('ALL_CHANGE'):
            change_group, _ = Group.objects.get_or_create(name='Update')
            change_perms = Permission.objects.filter(codename__startswith='change_')
            change_group.permissions.set(change_perms)
            user.groups.add(change_group)

        if self.cleaned_data.get('ALL_DELETE'):
            delete_group, _ = Group.objects.get_or_create(name='Delete')
            delete_perms = Permission.objects.filter(codename__startswith='delete_')
            delete_group.permissions.set(delete_perms)
            user.groups.add(delete_group)
