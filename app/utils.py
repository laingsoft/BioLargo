# generates a html table given headers and a queryset.
# Arguments:
# data : queryset of data.
# headers : headers of the table.
# classes : css classes for table. By default, it's only bootstrap's table class.
def to_table(data, headers, classes = ['table']):

    thead = ''.join(['<th scope="col">{0}</th>'.format(h) for h in headers])
    tbody = []

    for row in data:
        r = ''.join(['<td>{0}</td>'.format(row[h]) for h in headers])
        r = "<tr>{0}</tr>".format(r)
        tbody.append(r)

    tbody = ''.join(tbody)

    if classes:
        tclasses = "class='{0}'".format(' '.join(classes)) 

    else:
        tclasses = ''

    table = "<table {0}><thead><tr>{1}</tr></thead><tbody>{2}</tbody></table>".format(tclasses, thead, tbody)

    return table
