from rest_framework import status
from CrimeMapping.views import ukdf
from rest_framework.views import APIView
from rest_framework.response import Response

    
class CrimeAPI(APIView):
    def get(self, request, format=None):
        endDate = request.GET.get('param_to')
        Where = request.GET.get('param_where')
        Arrest = request.GET.get('param_arrest')
        startDate = request.GET.get('param_from')
        Domestic = request.GET.get('param_domestic')
        Type = request.GET.getlist('param_type', [])
        print(">>>>>>>>",startDate, endDate, Where, Arrest, Domestic, Type,  "<<<<<<<<<<<")

        crimex: dict = {
                'District':any,
                'Type':any,
                'Where':any,
                'selDistrict':"",
                'selType':"",
                'selWhere':"",
                'startDate':"",
                'endDate':"",
                'domestic':"",
                'arrest':"",
                'startendDates':"",
                }
        
        tempDF = ukdf.copy()
        crimex['selType'] = Type
        crimex['arrest'] = Arrest
        crimex['selWhere'] = Where
        crimex['endDate'] = endDate
        crimex['domestic'] = Domestic
        crimex['startDate'] = startDate
        crimex['Type']  = tempDF["Type"].unique()
        crimex['Where']  = tempDF["Where"].unique()
        crimex['District']  = tempDF["District"].unique()
        crimex['startendDates'] = str(startDate) + " - " + str(endDate)

        print(crimex,"<<<<< crime")
        return Response(crimex, status=status.HTTP_200_OK)

    # def post(self, request, format=None):
    #     if request.method == 'POST':
    #         param_value = request.GET.get('param_crime')
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
