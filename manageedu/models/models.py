# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class task(models.Model):
    _name = 'manageedu.task'
    _description = 'manageedu.task'

    code = fields.Char(compute="_get_code")
    name = fields.Char(string="Nombre", readonly=False, required=True, help="Introduzca el nombre") #Name
    description = fields.Text(string="Descripción")
    start_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")
    is_paused = fields.Boolean(string="¿Pausado?")
    sprint = fields.Many2one("manageedu.sprint", compute ="_get_sprint",store=True)
    history = fields.Many2one("manageedu.history", ondelete="set null", help="Historia relacionada")
    technologies = fields.Many2many(comodel_name="manageedu.technology",
                                    relation="technologies_tasks",
                                    column1="task_id",
                                    column2="technology_id")
    project = fields.Many2one("manageedu.project", related="history.project", readonly=True)
    code = fields.Char(compute="_get_code")
    priority = fields.Selection(
        [('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta')],
        string="Prioridad",
        default='medium',
    )

    
    @api.onchange('is_paused')
    def _onchange_is_paused(self):
        for task in self:
            if task.is_paused:
                task.priority = 'low'  
    
    
    # OTRA FORMA DE HACER LA FUNCIÓN CALCULAR FECHA
    # def _get_definition_date(self):
    #     return datetime.datetime.now()
    # definition_date = fields.Datetime(default=_get_definition_date)
    
    definition_date = fields.Datetime(default=lambda p: datetime.datetime.now())
    #@api.one
    def _get_code(self):
        for task in self:
            # try:
                task.code = "TSK_"+str(task.id)
                #_logger.info("Código generado: "+task.code)
            #except:
                #raise ValidationError(_("Generación de código errónea"))
                
    @api.depends('code')
    def _get_sprint(self):
        for task in self:
            sprints=self.env['manageedu.sprint'].search([('project.id','=',task.history.project.id)])
            found = False
            for sprint in sprints:
                if isinstance(sprint.end_date, datetime.datetime) and sprint.end_date > datetime.datetime.now():
                    task.sprint=sprint.id
                    found=True
            if not found:
                task.sprint = False




class sprint(models.Model):
    _name = 'manageedu.sprint'
    _description = 'manageedu.sprint'

    name = fields.Char(string="Nombre")
    description = fields.Text(string="Descripción")   
    duration = fields.Integer(default=15)
    start_date = fields.Datetime(string="Fecha inicio")    
    end_date = fields.Datetime(string="Fecha fin", compute="_get_end_date", store=True)
    tasks = fields.One2many(string="Tareas", comodel_name="manageedu.task", inverse_name='sprint')
    project = fields.Many2one("manageedu.project")

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for sprint in self:            
                if isinstance(sprint.start_date, datetime.datetime) and sprint.duration > 0:
                    sprint.end_date = sprint.start_date + datetime.timedelta(days=sprint.duration)
                else:
                    sprint.end_date = sprint.start_date



class project(models.Model):
    _name = 'manageedu.project'
    _description = 'manageedu.project'
    
    name = fields.Char(string="Nombre")
    description = fields.Text(string="Descripción")
    histories = fields.One2many(comodel_name="manageedu.history", inverse_name="project")
    sprints = fields.One2many(comodel_name="manageedu.sprint", inverse_name="project") #No estaba en el proyecto original


class history(models.Model):
    _name = 'manageedu.history'
    _description = 'manageedu.history'
    
    name = fields.Char(string="Nombre")
    description = fields.Text(string="Descripción")
    project = fields.Many2one("manageedu.project", ondelete="set null")
    tasks = fields.One2many(string="Tareas", comodel_name="manageedu.task", inverse_name="history")
    used_technologies = fields.Many2many("manageedu.technology", compute="_get_used_technologies")
    
    def _get_used_technologies(self):
        for history in self:
            technologies = None
            for task in history.tasks:
                if not technologies:
                    technologies=task.technologies
                else:
                    technologies=technologies+task.technologies
            history.used_technologies = technologies

class technology(models.Model):
    _name = 'manageedu.technology'
    _description = 'manageedu.technology'

    name = fields.Char(string="Nombre")
    description = fields.Text(string="Descripción")

    photo = fields.Image(string="Imagen", max_width=200, max_height=200)
    tasks = fields.Many2many(comodel_name="manageedu.task",
                             relation="technologies_tasks",
                             column1="technology_id",
                             column2="task_id")

class developer(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    is_dev = fields.Boolean()
    
    technologies = fields.Many2many('manageedu.technology',
                        relation="developer_technologies",
                        column1="developer_id",
                        column2="technologies_id")




# class manage(models.Model):
#     _name = 'manage.manage'
#     _description = 'manage.manage'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100