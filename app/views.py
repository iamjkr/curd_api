from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import json
from .forms import ProductForm

from django.core.serializers import serialize

from .models import Product

# using python inbuild json and django built in JsonResponse
class ViewAllProducts(View):
    def get(self,request):
        query = Product.objects.all()
        #reading data from database and returning a dictionary
        data = {} #empty dictionary
        for row in query:
            d1 = {
                row.no: {
                    "product_name": row.name,
                    "product_price": row.price,
                    "product_quntity": row.quantity,
                    "product_description": row.description
                }
            }
            data.update(d1)
            #using python built in json
            #converting dictionary to json format
            json_data = json.dumps(d1)
            print(json_data)
            return HttpResponse(json_data, content_type='application/json')
            #using JsonResponse

            # return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class InsertOneProduct(View):
    def post(self, request):
        #request.body will return binary string
        print(request.body)
        #to convert binary string to json format we use loads function in python built in json
        json_data = json.loads(request.body)
        print(json_data)
        #to save the data into database we need to create a form.
        forms =ProductForm(json_data)
        if forms.is_valid():
            forms.save()
            json_data = json.dumps({'success': 'Product added successfully'})
        else:
            json_data = json.dumps(forms.errors)
        return HttpResponse(json_data, content_type='application/json')


class ViewOneProduct(View):
    def get(self,request,pk):
        try:
            query = Product.objects.get(no=pk)
            data = {"product_name": query.name,
                    "product_price": query.price,
                    "product_quntity": query.quantity,
                    "product_description": query.description}
            json_data = json.dumps(data)
            print(json_data)
            #return HttpResponse(json_data, content_type='application/json')
        except Product.DoesNotExist:
            error_message = {"error":"Product does not exist"}
            json_data = json.dumps(error_message)
        return HttpResponse(json_data, content_type='application/json')

@method_decorator(csrf_exempt, name='dispatch')
class UpdateOneProduct(View):
    def put(self,request,pk):
        try:
            old_details = Product.objects.get(no=pk)
            new_details = json.loads(request.body)
            data = {
                'no': old_details.no,
                'name': old_details.name,
                'price': old_details.price,
                'quantity': old_details.quantity,
                'description': old_details.description
            }
            for key, value in new_details.items():
                data[key] = value
            form = ProductForm(data=data, instance=old_details)
            if form.is_valid():
                form.save()
                json_data = json.dumps({"success": "Product updated successfully"})
            else:
                json_data = json.dumps(form.errors)
            return HttpResponse(json_data, content_type='application/json')
        except Product.DoesNotExist:
            json_data = json.dumps({"error":"Product does not exist"})
            return HttpResponse(json_data, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class DeleteOneProduct(View):
    def delete(self, request, pk):
        try:
            del_product = Product.objects.get(no=pk).delete()
            if del_product[0] == 1:
                json_data = json.dumps({"success": "Product deleted successfully"})
                return HttpResponse(json_data, content_type='application/json')
        except Product.DoesNotExist:
            json_data = json.dumps({"error":"Product does not exist"})
            return HttpResponse(json_data, content_type='application/json')


#In this using django built in 'serializers'
class ViewProductsusingserializer(View):
    def get(self,request):
        query = Product.objects.all()
        json_data = serialize('json', query)
        return HttpResponse(json_data, content_type='application/json')


class ViewOneProductSer(View):
    def get(self, request, pk):
        try:
            query = Product.objects.get(no=pk)
            json_data = serialize('json', query)
            # return HttpResponse(json_data, content_type='application/json')
        except Product.DoesNotExist:
            error_message = {"error": "Product does not exist"}
            json_data = serialize('json', error_message)
        return HttpResponse(json_data, content_type='application/json')
