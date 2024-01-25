import os
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blogapp.models import BlogPost, Tag, TableOfContent

markdown_files_path = 'blogapp/blogs/'

def extract_front_matter(file_content):
    front_matter = {}
    match = re.match(r'^---\n(.*?)\n---\n(.*)', file_content, re.DOTALL)
    if match:
        front_matter_text, content = match.groups()
        front_matter_lines = front_matter_text.strip().split('\n')
        for line in front_matter_lines:
            key, value = line.split(':', 1)
            front_matter[key.strip()] = value.strip()

        content = process_code_blocks(content)
        content = process_table_of_contents(content)

    return front_matter, content
    
def process_code_blocks(content):
    language_classes = {
        'bash': 'mockup-code',
        'python': 'mockup-code',
        'html': 'mockup-code',
        'css': 'mockup-code',
        'js': 'mockup-code',
    }

    code_block_pattern = r'```(\w+)\n(.*?)```'

    def replace_code_block(match):
        language = match.group(1)
        code_lines = match.group(2).split('\n')
        
        # Check if the language has a corresponding DaisyCSS class, if not, use a default class
        daisy_class = language_classes.get(language, 'mockup-code')

        # Create a list to hold transformed code lines
        transformed_lines = []

        # Determine if it's a bash code or not
        is_base_code = language in ['bash']

        # Process each line of code and format it with the required HTML structure and DaisyCSS class
        for line in code_lines:
            if is_base_code:
                transformed_lines.append(f'<pre data-prefix="$"><code>{line}</code></pre>')
            else:
                transformed_lines.append(f'<pre><code>{line}</code></pre>')

        # Combine all transformed lines into a single block with proper indentation
        transformed_content = '\n'.join(transformed_lines)

        # Wrap the transformed content in the mockup-code div
        return f'<div class="{daisy_class}">\n{transformed_content}\n</div>'

    # Use regex substitution to replace code blocks with transformed HTML structure
    transformed_content = re.sub(code_block_pattern, replace_code_block, content, flags=re.DOTALL)

    return transformed_content

def process_table_of_contents(content):
    def replace_header(match):
        header = match.group(1)
        header_id = slugify(header)
        return f'<h2 id="{header_id}">{header}</h2>'

    # Replace '##' with HTML <h2> elements with IDs
    transformed_content = re.sub(r'^##\s+(.*)$', replace_header, content, flags=re.MULTILINE)
    
    return transformed_content
    
def extract_table_of_contents(file_content):
    table_of_contents = []
    frontmatter_started = False
    toc_started = False
    for line in file_content.split('\n'):
        if line.strip() == '---':
            if not frontmatter_started:
                frontmatter_started = True
            elif frontmatter_started and not toc_started:
                toc_started = True
        elif frontmatter_started and toc_started:
            if line.startswith("##"):
                match = re.search(r'^##\s+(.*)$', line)
                if match:
                    word = match.group(1)
                    table_of_contents.append(word)

    return table_of_contents

def extract_intro_content(file_content):
    intro_content = ""
    intro_started = False

    for line in file_content.split('\n'):
        if line.startswith("## Intro"):
            intro_started = True
        elif line.startswith("## "):
            if intro_started:
                break
        elif intro_started:
            intro_content += line + '\n'

    return intro_content.strip()

class Command(BaseCommand):
    help = 'Create or update blog posts based on changes in Markdown files'
    def handle(self, *args, **kwargs):
        try:
            existing_posts = BlogPost.objects.all()
            existing_slugs = {post.slug for post in existing_posts}

            self.process_markdown_files(existing_posts, existing_slugs)

            self.remove_missing_blog_posts(existing_slugs)
            self.remove_orphaned_tags()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
        
    def process_markdown_files(self, existing_posts, existing_slugs):
        for filename in os.listdir(markdown_files_path):
            if filename.endswith('.md'):
                with open(os.path.join(markdown_files_path, filename), 'r') as file:
                    file_content = file.read()
                    front_matter, content = extract_front_matter(file_content)
                    title = front_matter.get('Title', 'Untitled')
                    publish_date = front_matter.get('Published Date', '')
                    last_update = front_matter.get('Last Update', '')
                    tags_list = front_matter.get('Tags', '').split(', ')
                    toc_list = extract_table_of_contents(file_content)
                    intro = extract_intro_content(file_content)

                    if publish_date is None or publish_date == '':
                        publish_date = datetime.strptime(publish_date, '%Y-%m-%d').date()

                    slug = slugify(title)
                    existing_slugs.discard(slug)

                    self.update_or_create_post(
                        existing_posts,
                        slug,
                        title,
                        content,
                        publish_date,
                        last_update,
                        tags_list,
                        toc_list,
                        intro
                    )
            else:
                self.stdout.write(self.style.WARNING(f'Skipping file: {filename}'))
                

    def update_or_create_post(self, existing_posts, slug, title, content, publish_date, last_update, tags_list, toc_list, intro):
        matching_posts = existing_posts.filter(slug=slug)

        if matching_posts.exists():
            # Update existing post
            self.update_post(matching_posts.first(), title, content, publish_date, last_update, tags_list, toc_list, intro)
        else:
            # Create new post
            self.create_post(title, content, publish_date, last_update, slug, tags_list, toc_list, intro)

    def update_post(self, post, title, content, publish_date, last_update, tags_list, toc_list, intro):
        if (
            post.title != title
            or post.content != content
            or post.publish_date != publish_date
            or post.last_update != last_update
            or post.toc.count() != len(toc_list)
            or post.tags.count() != len(tags_list)
            or post.intro != intro
        ):
            post.title = title
            post.content = content
            post.publish_date = publish_date
            post.last_update = last_update
            post.intro = intro
            post.toc.clear()
            post.tags.clear()

            for tag_name in tags_list:
                name, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(name)

            index = 1
            for toc_name in toc_list:
                content, created = TableOfContent.objects.get_or_create(content=toc_name, order=index, slug=slugify(toc_name))
                post.toc.add(content)
                index += 1

            post.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated post: {title}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'No changes detected for post: {title}'))

    def create_post(self, title, content, publish_date, last_update, slug, tags_list, toc_list, intro):
        new_post = BlogPost(
            title=title,
            content=content,
            publish_date=publish_date,
            last_update=last_update,
            slug=slug,
            intro=intro
        )
        new_post.save()

        index = 1
        for toc_name in toc_list:
            content, created = TableOfContent.objects.get_or_create(content=toc_name, order=index, slug=slugify(toc_name))
            new_post.toc.add(content)
            index += 1

        for tag_name in tags_list:
            name, created = Tag.objects.get_or_create(name=tag_name)
            new_post.tags.add(name)

        new_post.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created post: {title}'))

    def remove_missing_blog_posts(self, existing_slugs):
        if existing_slugs:
            BlogPost.objects.filter(slug__in=existing_slugs).delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted missing blog posts: {existing_slugs}'))

    def remove_orphaned_tags(self):
        orphaned_tags = Tag.objects.filter(blogpost=None)
        if orphaned_tags:
            orphaned_tags.delete()
            self.stdout.write(self.style.SUCCESS('Deleted orphaned tags'))
