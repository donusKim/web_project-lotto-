import uuid
from django.db import models
from django.urls import reverse
# Create your models here.
def money2readble(money):
    money=str(money)
    money_len=len(money)
    if money_len<5:
        return money+'원'
    elif money_len<9:
        return money[0:money_len-4]+'만 '+money[money_len-4:money_len]+'원'
    elif money_len<13:
        return money[0:money_len-8]+'억 '+money[money_len-8:money_len-4]+'만 '+money[money_len-4:money_len]+'원'
    elif money_len<17:
        return money[0:money_len-12]+'조 '+money[money_len-12:money_len-8]+'억 '+money[money_len-8:money_len-4]+'만 '+money[money_len-4:money_len]+'원'


class Round(models.Model):
    round_num = models.IntegerField(help_text='Number of round', primary_key=True)
    first_win_num = models.IntegerField(help_text='First winning number of the round')
    second_win_num = models.IntegerField(help_text='Second winning number of the round')
    third_win_num = models.IntegerField(help_text='Third winning number of the round')
    fourth_win_num = models.IntegerField(help_text='Fourth winning number of the round')
    fifth_win_num = models.IntegerField(help_text='Fifth winning number of the round')
    sixth_win_num = models.IntegerField(help_text='Sixth winning number of the round')
    bonus_num = models.IntegerField(help_text='Bonus number of the round')
    first_win_money = models.BigIntegerField(help_text='Total winning money for first place')
    second_win_money = models.BigIntegerField(help_text='Total winning money for second place')
    third_win_money = models.BigIntegerField(help_text='Total winning money for third place')
    fourth_win_money = models.BigIntegerField(help_text='Total winning money for fourth place')
    fifth_win_money = models.BigIntegerField(help_text='Total winning money for fifth place')
    num_first_winner = models.IntegerField(help_text='Number of first place winner')
    num_second_winner = models.IntegerField(help_text='Number of second place winner')
    num_third_winner = models.IntegerField(help_text='Number of third place winner')
    num_fourth_winner = models.IntegerField(help_text='Number of fourth place winner')
    num_fifth_winner = models.IntegerField(help_text='Number of fifth place winner')
    num_auto = models.IntegerField(help_text='Number of winner by auto type', blank=True, null=True)
    num_manual = models.IntegerField(help_text='Number of winner by manual type', blank=True, null=True)
    num_halfauto = models.IntegerField(help_text='Number of winner by halfauto type', blank=True, null=True)
    first_stores = models.ManyToManyField('Store', help_text='Stores that won first place', blank=True,
                                          related_name='first_stores')
    second_stores = models.ManyToManyField('Store', help_text='Stores that won second place', blank=True,
                                           related_name='second_stores')

    @property
    def get_win_info(self):
        win_moneys = [self.first_win_money, self.second_win_money, self.third_win_money, self.fourth_win_money,
                    self.fifth_win_money]
        num_winners = [self.num_first_winner, self.num_second_winner, self.num_third_winner, self.num_fourth_winner,
                    self.num_fifth_winner]
        results = []
        for i in range(5):
            info = []
            info.append(i+1)
            info.append(money2readble(win_moneys[i]))
            info.append(money2readble(int(win_moneys[i]/num_winners[i])))
            info.append(num_winners[i])
            results.append(info)
        return results

    @property
    def get_range_cnt(self):
        win_nums = [self.first_win_num, self.second_win_num, self.third_win_num, self.fourth_win_num, self.fifth_win_num, self.sixth_win_num]
        results = []
        for i in range(1, 6):
            cnt = 0
            lower = 10*(i-1)
            upper = 10*i
            for num in win_nums:
                if num >= lower and num < upper:
                    cnt += 1
            results.append(cnt)
        return results


    def get_first_money_per_winner(self):
        if self.num_first_winner:
            return int(self.first_win_money/self.num_first_winner)
        return 0

    def get_second_money_per_winner(self):
        if self.num_second_winner:
            return int(self.second_win_money / self.num_second_winner)
        return 0

    def get_third_money_per_winner(self):
        if self.num_third_winner:
            return int(self.third_win_money / self.num_third_winner)
        return 0
    def get_num_sum(self):
        return self.first_win_num+self.second_win_num+self.third_win_num+self.fourth_win_num+self.fifth_win_num+self.sixth_win_num
    def get_oddity(self):
        if self.get_num_sum()%2:
            return "홀"
        return "짝"
    def __str__(self):
        """String for representing the Model object."""
        return str(self.round_num)+"회차"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('round-detail', args=[str(self.round_num)])

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this store')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True)
    first_place = models.ManyToManyField(Round, help_text='Round that the store won first place on 645 lotto',
                                         related_name='first', blank=True)
    second_place = models.ManyToManyField(Round, help_text='Round that the store won second place on 645 lotto',
                                          related_name='second', blank=True)
    opened = models.BooleanField(default=True, help_text='whether store is currently opened or not')
    serve_645Lotto = models.BooleanField(default=True, help_text='whether store serves 645 lotto or not')
    serve_pensionLotto = models.BooleanField(default=False, help_text='whether store serves pension lotto or not')
    serve_speatto = models.BooleanField(default=False, help_text='whether store serves speatto or not')
    """
    추후에 연금로또와 스피또 당첨 정보도 넣어야함,,,
    """

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('store-detail', args=[str(self.id)])