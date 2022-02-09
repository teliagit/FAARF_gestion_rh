from odoo import fields, api, models, tools, _
import string
from datetime import datetime, date
import pdb
import calendar
from calendar import monthrange
from odoo.exceptions import UserError, ValidationError
from math import *


# Creation de la classe fonction avec ses attributs
class HrFonction(models.Model):
    _name = "hr_fonctionss"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

# Creation de la classe emploi avec ses attributs
class HrEmploi(models.Model):
    _name = "hr_emploi"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

class HrDepartment(models.Model):
    _inherit = 'hr.department'
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",default=lambda self: self.env.user.company_id.id)
    code = fields.Char(string = "Code", required=True)

# Creation de la classe service avec ses attributs
class RefService(models.Model):
    _name = "hr_service"
    x_direction_id = fields.Many2one('hr.department', 'Département/Direction', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    est_stock = fields.Selection([
        ('1', 'Oui'),
        ('2', 'Non'),
    ], string="Est Service du Stock ?", default='2', required=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# Creation de la classe unité avec ses attributs
class RefUnite(models.Model):
    _name = "hr_unite"
    x_service_id = fields.Many2one('hr_service', 'Service', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# Creation de la classe section avec ses attributs
class RefSection(models.Model):
    _name = "hr_section"
    x_unite_id = fields.Many2one('hr_unite', 'Unité', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    responsable = fields.Many2one('res.users', string='Responsable')

# heritage type de contrat
class HrTypeContrats(models.Model):
    _name = 'hr_contract_type'

    name = fields.Char(string='Name', required=False)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)

# Creation de la classe nature  precompte avec ses attributs
class HrNature(models.Model):
    _name = "hr_nature"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of nature.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

# Creation de la classe motif cessation avec ses attributs
class HrMotif(models.Model):
    _name = "hr_motif"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of motif.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

# creation table pour contenir le nombre d'année de depart a la retraite des employés
class HrNbreAnnee(models.Model):
    _name = 'hr_nbreannee'
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
    name = fields.Integer(string="Nombre année", required=True)

# Creation de la classe grille des contractuels du burkina faso avec ses attributs
class HrGrilleSalarialeContractuel(models.Model):
    _name = "hr_grillesalariale_contractuel"
    _rec_name = "x_salbase_ctrt"
    x_class_c_id = fields.Many2one('hr_classe', string='Classe')
    x_indice_c = fields.Float(string="Indice")
    x_categorie_c_id = fields.Many2one('hr_categorie', string='Catégorie', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_echellon_c_id = fields.Many2one('hr_echellon', string='Echelon', required=True)
    x_salbase_ctrt = fields.Float(string="Salaire Base", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    active = fields.Boolean(string="Etat", default=True)

class HrCritereEvalaution(models.Model):
    _name = "hr_critere_evaluation"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Critères Evalauation.", default=10)
    name = fields.Char(string="Libelle long", required=True)
    lib_court = fields.Char(string="Libelle court")
    active = fields.Boolean(string="Etat", default=True)
    description = fields.Text(string="Description", size="1000")

class HrSousCritereEvaluation(models.Model):
    _name = 'hr_sous_critere_evaluation'
    _order = 'sequence, id'
    _rec_name = "lib_long"

    sequence = fields.Integer(help="Gives the sequence when displaying a list of Sous Critères Evalauation.",
                              default=10)
    name = fields.Char(string="Borne inférieure")
    born_sup = fields.Char(string="Borne supérieure")
    lib_court = fields.Char(string="Libelle court")
    lib_long = fields.Char(string="Libelle long")
    lib_p = fields.Char(string="Concat.")
    note_sous_critere = fields.Float(string="Note", required=True)
    x_critere_evaluation_id = fields.Many2one('hr_critere_evaluation', string='Choisir Critère', required=True)
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)

    # fonction de concatenation
    @api.onchange('name', 'born_sup')
    def _concat(self):
        for tests in self:
            tests.lib_p = "Taux compris entre " + str(tests.name) + " et " + str(tests.born_sup) + "%"

# Creation de la classe titre avec ses attributs
class HrTitreEvaluation(models.Model):
    _name = "hr_titreevaluation"
    _order = 'sequence, id'
    _rec_name = 'lib_long'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of nature.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

# Creation de la classe IndemniteAstreinte avec ses attributs
class HrParametrageIndemniteAstreinte(models.Model):
    _name = "hr_paramindemniteastr"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité astreinte")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')