from . import models
from .import serializers

class CarServices:
    @classmethod
    def get_car(cls, code_id):
        response = serializers.ResponseSerializers()
        if code_id is None or code_id.isspace():
            response.addErrorMessage(999,'param is incorrect')
            return response
        
        cars = models.Car.objects.filter(code=code_id)
        if len(cars) <= 0:
            response.addErrorMessage(404,'Not found.')
            return response
        data_result = serializers.ViewCarSerializers(cars[0])
        response.data = data_result.data
        return response