import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_minimum_points():
    question = Question(title='q1', points=1)
    assert question.points == 1

def test_create_question_with_maximum_points():
    question = Question(title='q1', points=100)
    assert question.points == 100


def test_create_choice_with_empty_text():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('', False)

def test_create_choice_with_text_too_long():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)

def test_add_multiple_choices():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    assert len(question.choices) == 3

def test_choice_ids_are_sequential():
    question = Question(title='q1')

    first = question.add_choice('a')
    second = question.add_choice('b')
    third = question.add_choice('c')

    assert first.id == 1
    assert second.id == 2
    assert third.id == 3

def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_choice_by_id(1)

    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    first = question.add_choice('a')
    second = question.add_choice('b')
    third = question.add_choice('c')

    question.set_correct_choices([first.id, third.id])

    assert first.is_correct
    assert not second.is_correct
    assert third.is_correct

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)

    first = question.add_choice('a', True)
    second = question.add_choice('b', False)
    third = question.add_choice('c', True)

    result = question.correct_selected_choices(
        [first.id, second.id]
    )
    assert result == [first.id]

@pytest.fixture
def question_with_choices():
    question = Question(title='Python', max_selections=2)

    question.add_choice('Python', True)
    question.add_choice('Java', False)
    question.add_choice('C++', True)

    return question


def test_fixture_correct_selected_choices(question_with_choices):
    question = question_with_choices

    result = question.correct_selected_choices([1, 2])

    assert result == [1]


def test_fixture_remove_choice(question_with_choices):
    question = question_with_choices

    question.remove_choice_by_id(2)

    assert len(question.choices) == 2
    assert [choice.text for choice in question.choices] == [
        'Python', 'C++'
    ]
