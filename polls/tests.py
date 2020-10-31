from django.test import TestCase
import datetime

from django.utils import timezone
from .models import Question
from django.urls import reverse

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexIveeweTests(TestCase):
    def test_no_questions(self):
        #questionが存在しなかったら適切なメッセージを表示させる
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questionn(self):
        #pub_dateが過去のquestionはindexページに表示される
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        #pub_dateが将来の日付のquestionはindexに表示されない
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        #pub_dateが将来の物と過去の物が両方存在したら、過去の方だけ表示させる
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_question(self):
        #indexページには複数のquestionが表示される
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDatailViewTests(TestCase):
    def test_future_question(self):

        #将来のquestionは404を返す
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response  =self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        #過去ものもは普通に表示される
        past_question = create_question(question_text="Past Question", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        #将来の日付はfalseを返すべき
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        #ここのselfは何?

    def test_was_publisehd_recently_with_old_question(self):
        #1日以上経過してたらout 
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        #経過時間が1日未満ならOK
        #今から23時間59分59秒分の時間を引いてる(昨日から1日経ってない)
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# Create your tests here.
