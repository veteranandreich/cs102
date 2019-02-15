<!-- news_template.tpl -->
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
                <th colspan="3">Label</th>
            </thead>
            <style>
            .maybe{
                color:blue;
            }
            .good{
                color:green;
            }
            .never{
                color:red;
            }
            </style>
            <tbody>
                %for row in good:
                <tr>
                    <td><a class = "good" href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row.id }}&classify=True">интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row.id }}&classify=True">возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row.id }}&classify=True">неинтересно</a></td>
                </tr>
                %end
                %for row in maybe:
                <tr>
                    <td><a class="maybe" href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row.id }}&classify=True">интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row.id }}&classify=True">возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row.id }}&classify=True">неинтересно</a></td>
                </tr>
                %end
                %for row in never:
                <tr>
                    <td><a class = "never" href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row.id }}&classify=True">интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row.id }}&classify=True">возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row.id }}&classify=True">неинтересно</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/news" class="ui right floated small primary button">Back to the main table</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
