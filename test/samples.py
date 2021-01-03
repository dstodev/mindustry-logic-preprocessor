from inspect import cleandoc

STANDARD_SIMPLE = cleandoc('''
    jump 3 notEqual @unit null
    ubind @mono
    end
''')

CUSTOM_SIMPLE = cleandoc('''
    jump :label1 notEqual @unit null
    ubind @mono
    label1:
    end
''')
