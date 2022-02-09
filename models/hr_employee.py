from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # Nationalité & Autre Information
    x_nationalite_id = fields.Many2one('ref_nationalite', default=lambda self: self.env['ref_nationalite'].search(
        [('code_nationalite', '=', 'BF')]), string='Nationalité')
    matricule_genere = fields.Char(string="Matricule")
    matricule = fields.Char(string="Mle Fonctionnaire ")
    x_type_piece_id = fields.Many2one("hr_typepiece", string="Type pièce", required=True)
    ref_identification = fields.Char(string='Ref.Identification', required=True)
    # Information de  contact
    tel = fields.Char(string='Telephone', required=True)
    personne_id = fields.Char('Personne à prevenir en cas de besoin', required=True)
    x_email = fields.Char(string="Email")
    # Statut
    genre = fields.Selection([
        ('masculin', 'Masculin'),('feminin', 'Feminin'),
        ('autre', 'Autre')],
        string='Genre', default="masculin")
    situation_marital = fields.Selection([
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('concubinage', 'Concubinage'),
        ('veuf(ve)', 'Veuf(ve)'),
        ('divorce', 'Divorcé(e)')],
        string='Etat civil', default="celibataire")
    charge_femme = fields.Integer(string="Charge femme", required=True)
    charge_enfant = fields.Integer(string="Charge enfant", required=True)
    charge = fields.Integer(store=True, string="Charge total", readonly=True)
    # Naissance
    x_date_naissance = fields.Date(string='Date de naissance', required=True)
    x_nb_annee_retraite = fields.Many2one("hr_nbreannee", string="Age de retraite", required=True)
    lieu_naiss = fields.Many2one('ref_localite', string='Lieu de naissance')
    # Éducation
    x_diplome_id = fields.Many2one("hr_diplome", string="Dernier diplôme")
    x_diplome_recrut_id = fields.Many2one("hr_diplome", string="Diplôme de recrutement")
    branche = fields.Char(string="Branche d'étude")
    ecole = fields.Char(string="Ecole/Université")
    observations = fields.Html(string='Observations')