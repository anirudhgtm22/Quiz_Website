from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz
from django.utils import timezone
import json
from django.views.generic import TemplateView




class HomePageView(TemplateView):
    template_name = 'home.html'
    
    
@csrf_exempt
def create_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        question = data.get('question')
        options = data.get('options', [])
        right_answer = data.get('rightAnswer')
        start_date = data.get('startDate')
        end_date = data.get('endDate')

        if not question:
            return JsonResponse({'error': 'question field is required'}, status=400)

        if not options:
            return JsonResponse({'error': 'options field is required'}, status=400)

        if right_answer is None or right_answer == '':
            return JsonResponse({'error': 'rightAnswer field is required'}, status=400)

        try:
            right_answer = int(right_answer)
        except ValueError:
            return JsonResponse({'error': 'rightAnswer field must be an integer'}, status=400)

        if not start_date:
            return JsonResponse({'error': 'startDate field is required'}, status=400)

        if not end_date:
            return JsonResponse({'error': 'endDate field is required'}, status=400)

        quiz = Quiz(question=question, options=options, right_answer=right_answer,
                    start_date=start_date, end_date=end_date)
        quiz.save()

        return JsonResponse({'message': 'Quiz created successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



def get_active_quiz(request):
    current_time = timezone.now()
    active_quiz = Quiz.objects.filter(start_date__lte=current_time, end_date__gt=current_time, status='active')
    quizzes = []
    for quiz in active_quiz:
        quiz_data = {
            'question': quiz.question,
            'options': quiz.options,
            'rightAnswer': quiz.right_answer,
            'startDate': quiz.start_date,
            'endDate': quiz.end_date
        }
        quizzes.append(quiz_data)
    return JsonResponse(quizzes, safe=False)


def get_quiz_result(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    if quiz.status != 'finished':
        return JsonResponse({'error': 'Quiz result not available yet'}, status=400)

    result = {'rightAnswer': quiz.right_answer}
    return JsonResponse(result)


def get_all_quizzes(request):
    quizzes = Quiz.objects.all()
    quiz_list = []
    for quiz in quizzes:
        quiz_data = {
            'question': quiz.question,
            'options': quiz.options,
            'rightAnswer': quiz.right_answer,
            'startDate': quiz.start_date,
            'endDate': quiz.end_date
        }
        quiz_list.append(quiz_data)
    return JsonResponse(quiz_list, safe=False)
