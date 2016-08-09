from django.shortcuts import render

def render_result(request,article_dict):
	"""This function renders the html with th result."""

	s = str(
            render(
                request,
                'news.html',
                article_dict,
                content_type='text/html'))
        x = s.replace('u&#39;', '"')  # removing unicode issues in JS
        y = x.replace('&#39;', '"')
        z = y.replace('Content-Type: text/html', '')
        p = z.replace('u&quot;',"'")
        q = p.replace('&quot;',"'")
        return q