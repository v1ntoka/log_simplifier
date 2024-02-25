from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile


def create_temp_file(file):
    logfile = None
    if isinstance(file, TemporaryUploadedFile):
        logfile = open(file.temporary_file_path(), 'r', encoding='utf-8')
    elif isinstance(file, InMemoryUploadedFile):
        logfile = bytes.decode(file.read()).split('\n')

    with open('temp_file.txt', 'w', encoding='utf-8') as temp:
        for line in logfile:
            temp.write(line)
    if isinstance(file, TemporaryUploadedFile):
        file.close()
