from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'is_visitor']

# class UserForm(forms.ModelForm):
# 	class Meta:
# 		model = User
# 		fields = '__all__'

# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
		
# 		self.helper = FormHelper()
# 		self.helper.form_method = 'post'
# 		self.helper.layout = Layout(
# 			Row(
# 				Column('username', css_class='form-group col-md-3 mb-0'),
# 				Column('is_visitor', css_class='form-group col-md-3 mb-0'),
# 				Column('is_recepcionist', css_class='form-group col-md-3 mb-0'),
# 				Column('is_funsionariu', css_class='form-group col-md-3 mb-0'),
# 			),
# 			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Update"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
# 			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
# 		)
