var studios, films, directors;

var $factsTable = $('#factsTable');
function addFact(fact) {
    $factsTable.slideDown();
    $factsTable.append(Mustache.render(factTemplate, fact));
}

var $modalDiv = $('#modalTarget');
function addModal(template, data) {
    $modalDiv.html(Mustache.render(template, data));
}

$(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)
                && !this.crossDomain) {
                xhr.setRequestHeader("Content-Type", "application/json")
            }
        }
    });
    $('#loadFilesBtn').prop('disabled', true);
    $('#textSearchField').prop('disabled', true);
    $('#wordTextRadio1').prop('checked', true);

    $.ajax({
        type:'get',
        url:'/api/facts/',
        success: function (data) {
            var facts = data.facts;
            $.each(facts, function (i, fact) {
                addFact(fact);
            });

            $.get('/api/dimensions_names/', function (data) {
                projects = data.data.projects;
                customers = data.data.customers;
                teams = data.data.teams;
            });
        }
    });
});


//region POSTING

$('#newInstanceBtn').on('click', function () {

        var data = {
            modal: {
                type: "Create instance",
                header: "Create instance",
                classType: "createBtn"
            },
            fact: {
                projects: projects,
                customers: customers,
                teams: teams
            }
        };

        addModal(cuModalTemlate, data);
});

$modalDiv.delegate('.createBtn', 'click', function () {

     var data = {
        id_project:$('#projectSelect').val(),
        id_customer:$('#customerSelect').val(),
        id_team:$('#teamSelect').val()
    };

    $.ajax({
        type:'post',
        url:'/api/facts/',
        contentType:'application/json',
        data:JSON.stringify(data),
        dataType:'json',
        success:function (result) {
            addFact(result.fact)
        },
        error: function () {
            alert("Error while posting data!")
        }
    });
});

//endregion

//region DELETING

$factsTable.delegate('.deleteBtnModal', 'click', function () {
    var data = {
        id:$(this).attr('data-id'),
        type:"Delete instance",
        classType:"deleteBtn"
    };

    addModal(deletingModalTemplate, data)
});

$modalDiv.delegate('.deleteBtn','click', function () {
    var id = $(this).attr('data-id');
    var $tr = $('#fact'+id);
    $.ajax({
        type:'delete',
        url:'/api/facts/' + id+'/',
        success:function () {
            $tr.fadeOut(500, function () {
                $(this).remove();
            });
        },
        error: function () {
            alert("Error while deleting data!")
        }
    });
});

//endregion

//region EDITING

$factsTable.delegate('.updateBtnModal','click', function () {

    var id = $(this).attr('data-id');
    var $fact =$('#fact'+id).children();
    var dimensions = [
        $fact[1].textContent,
        $fact[2].textContent,
        $fact[3].textContent
    ];

     var projectsN = projects.slice(),
        customersN = customers.slice(),
        teamsN = teams.slice();
    projectsN = changedArray(projectsN, dimensions[0]);
    customersN = changedArray(customersN, dimensions[1]);
    teamsN = changedArray(teamsN, dimensions[2]);

    var data = {
        modal: {
            id: $(this).attr('data-id'),
            header:"Update instance",
            type: "Update",
            classType: "updateBtn"
        },
        fact:{
            projects:projectsN,
            customers:customersN,
            teams:teamsN
        }
    };

    addModal(cuModalTemlate, data);

});

function changedArray( array, name) {
    array.unshift(array.splice(array.findIndex(function (obj) {
        return obj.name === name;
    }),1)[0]);
    return array;
}

$modalDiv.delegate('.updateBtn', 'click', function () {

    var selected = [
        project=$('#projectSelect'),
        customer=$('#customerSelect'),
        team=$('#teamSelect')
    ];
    var data = {
        id_project:selected[0].val(),
        id_customer:selected[1].val(),
        id_team:selected[2].val()
    },
        id = $(this).attr('data-id');

    $.ajax({
        type:'put',
        url:'/api/facts/' + id +'/',
        contentType:'application/json',
        data:JSON.stringify(data),
        dataType:'json',
        success:function (result) {
            var fact = $('#fact'+id).children();
            fact[1].textContent =result.fact['id_project__project_name'];
            fact[2].textContent = result.fact['id_customer__customer_name'];
            fact[3].textContent = result.fact['id_team__team_name']
        },
        error: function () {
            alert("Error while updating data!")
        }
    });
});

//endregion

//region TRUNCATE

$('#truncateBtnModal').on('click', function () {

    var data = {
        type:"Truncate table",
        classType:"truncateBtn"
    };

    addModal(deletingModalTemplate, data)
});

$modalDiv.delegate('.truncateBtn', 'click', function () {
    $('#loadFilesBtn').prop('disabled', false);
    $.ajax({
        type:'delete',
        url:'/api/facts/',
        success:function () {
            $factsTable.fadeOut(600, function () {
                $(this).children().remove();
            })
        },
        error: function () {
            alert("Error while truncating table!")
        }
    });
});


//endregion

//region SEARCH

//region BOOL

$('#searchFinished').on('click', function () {

    var value = $('#finished').val();
    $('#searchFinishedTable').show();
    $.ajax({
        type: 'get',
        url: '/api/search/projects/?finish_status='+value,
        success:function (result) {
        console.log(result)
            $('#searchFinishTBody').children().remove();
            $.each(result.projects, function (i, obj) {
                $('#searchFinishTBody').append(Mustache.render(finishedTemplate, obj));
            });
        }
    });
});

//endregion

//region Date RANGE

$('#searchRange').on('click', function () {

    var bottom = $('#bottomVal').val(),
        top = $('#topVal').val();
    $('#searchRangeTable').show();
    $.ajax({
        type:'get',
        url:'/api/search/customers/?bottom='+bottom+
            '&top='+top,
        success:function (result) {
            $('#searchRangeTBody').children().remove();
            $.each(result.customers, function (i, obj) {
                $('#searchRangeTBody').append(Mustache.render(rangeTemplate, obj));
            });
        }
    });
});

//endregion

//endregion

//region TEMPLATES

var factTemplate =
    "<tr id='fact{{id_changing}}'>" +
    "   <td class='col-md-1'>{{id_changing}}</td>" +
    "   <td>{{id_project__project_name}}</td>" +
    "   <td>{{id_customer__customer_name}}</td>" +
    "   <td>{{id_team__team_name}}</td>" +
    "   <td>{{changing_date}}</td>" +
    "   <td class='col-md-3 text-center'>" +
    "       <button data-id='{{id_changing}}' class='updateBtnModal btn btn-info btn-sm'" +
    "               data-toggle='modal' data-target='#cuModal'>Edit</button>\n" +
    "       <button data-id='{{id_changing}}' class='deleteBtnModal btn btn-danger btn-sm'" +
    "               data-toggle='modal' data-target='#deletingModal'>Delete</button>" +
    "   </td>" +
    "</tr>";

var finishedTemplate =
    "<tr>" +
    "   <td class='col-md-1'>{{id_project}}</td>" +
    "   <td>{{id_project__project_name}}</td>" +
    "   <td class='col-md-6'>{{id_project__project_description}}</td>"+
    "</tr>";

var rangeTemplate =
    "<tr>" +
    "   <td class='col-md-1'>{{id_customer}}</td>" +
    "   <td>{{id_customer__customer_name}}</td>" +
    "   <td>{{id_customer__customer_email}}</td>" +
    "   <td>{{id_customer__invitings_date}}</td>"+
    "</tr>";

var deletingModalTemplate =
    '<div class="modal fade" id="deletingModal" role="dialog">\n' +
    '   <div class="modal-dialog modal-sm">\n' +
    '       <div class="modal-content">\n' +
    '           <div class="modal-header">\n' +
    '               <button type="button" class="close" data-dismiss="modal">&times;</button>\n' +
    '               <h4 class="modal-title">{{type}}!</h4>\n' +
    '           </div>\n' +
    '           <div class="modal-body">\n' +
    '               <p>Are you sure?</p>\n' +
    '           </div>\n' +
    '           <div class="modal-footer">\n' +
    '               <button data-id="{{id}}" class="{{classType}} btn btn-danger"' +
    '                       data-dismiss="modal">Delete</button>'+
    '               <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\n' +
    '           </div>\n' +
    '       </div>\n' +
    '   </div>\n' +
    '</div>';

var cuModalTemlate =
    '<div class="modal fade" id="cuModal" role="dialog">\n' +
    '   <div class="modal-dialog modal-md">\n' +
    '       <div class="modal-content">\n' +
    '           <div class="modal-header">\n' +
    '               <button type="button" class="close" data-dismiss="modal">&times;</button>\n' +
    '               <h4 class="modal-title">{{modal.header}}</h4>\n' +
    '           </div>\n' +
    '           <div class="modal-body">\n' +
    '               <form class="form-horizontal">\n' +
    '                   <div class="form-group">\n' +
    '                       <label class="control-label col-sm-2" for="projectSelect">Project:</label>\n' +
    '                           <div class="col-sm-10">\n' +
    '                               <select class="form-control" id="projectSelect">\n' +
    '                                   {{#fact.projects}}' +
    '                                       <option value="{{ id_project }}">{{ id_project__project_name }}</option>\n'+
    '                                   {{/fact.projects}}' +
    '                               </select>\n' +
    '                           </div>\n' +
    '                   </div>\n' +
    '                   <div class="form-group">\n' +
    '                       <label class="control-label col-sm-2" for="customerSelect">Customer:</label>\n' +
    '                           <div class="col-sm-10">\n' +
    '                               <select class="form-control" id="customerSelect">\n' +
    '                                   {{#fact.customers}}' +
    '                                       <option value="{{ id_customer }}">{{ id_customer__customer_name }}</option>\n'+
    '                                   {{/fact.customers}}' +
    '                               </select>\n' +
    '                           </div>\n' +
    '                   </div>\n' +
    '                   <div class="form-group">\n' +
    '                       <label class="control-label col-sm-2" for="teamSelect">Team:</label>\n' +
    '                           <div class="col-sm-10">\n' +
    '                               <select class="form-control" id="teamSelect">\n' +
    '                                   {{#fact.teams}}' +
    '                                       <option value="{{ id_team }}">{{ id_team__team_name }}</option>\n'+
    '                                   {{/fact.teams}}' +
    '                               </select>\n' +
    '                           </div>\n' +
    '                   </div>\n' +
    '                   <div class="form-group">\n' +
    '                       <div class="col-sm-offset-2 col-sm-10">\n' +
    '                           <button data-id="{{modal.id}}" type="button" class="{{modal.classType}} ' +
    '                                   btn btn-primary" data-dismiss="modal">{{modal.type}}</button>' +
    '                       </div>\n' +
    '                   </div>\n' +
    '              </form>' +
    '           </div>\n' +
    '           <div class="modal-footer">\n' +
    '               <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\n' +
    '           </div>\n' +
    '       </div>\n' +
    '   </div>\n' +
    '</div>';

//endregion