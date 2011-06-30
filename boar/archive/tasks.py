from celery.task import task
import re
import subprocess

@task
def generate_page_image(page_id):
    from boar.archive.models import Page
    page = Page.objects.get(id=page_id)
    if not subprocess.call(['convert', '-density', '300', unicode(page.pdf.path), '-colorspace', 'RGB', unicode(re.sub(r'\.pdf$', '.jpg', page.pdf.path))]):
        page.image = re.sub(r'\.pdf$', '.jpg', unicode(page.pdf))
        page.save()


