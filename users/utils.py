import random, string

def random_code_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_invite_code_generator(instance, size=20, new_code=None):
    
    if new_code is not None:
        code = new_code
    else:
        code = random_code_generator(size=size)
    
    Pclass = instance.__class__
    code_exists = Pclass.objects.filter(inviteCode=code).exists()
    if code_exists:
        print('exists')
        new_code = random_code_generator(size=size)
        return unique_invite_code_generator(instance, size, new_code)
    return code