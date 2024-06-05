from models_only.models import Farmer, Searcher, PolicyMaker


def get_user_by_email(email):
    user_models = [
        (Farmer, 'farmer'),
        (Searcher, 'searcher'),
        (PolicyMaker, 'policy_maker')
    ]
    
    for model, user_type in user_models:
        try:
            user = model.objects.get(email=email)
            return user, user_type
        except model.DoesNotExist:
            continue
            
    return None, None