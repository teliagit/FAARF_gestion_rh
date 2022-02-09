from datetime import date

from odoo import fields, models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    date_signature = fields.Date(string="Date signature acte/decision d'engagement")

    # Situation administrative de l'agent dans l'Etat
    x_classees_id = fields.Many2one('hr_classe', string='Classe')
    x_categorie_id = fields.Many2one('hr_categorie', string='Catégorie')
    x_echelle_id = fields.Many2one('hr_echelle', string='Echelle')
    x_echellon_id = fields.Many2one('hr_echellon', string='Echelon')
    x_classification = fields.Char(store=True, string="Classification")
    date_modiff = fields.Date(string='Date effet', default=date.today())
    date_debut = fields.Date(string="Date d'engagement", default=date.today())
    date_fin = fields.Date(string="Date fin")
    x_solde_indiciaire = fields.Float(string="Solde Indiciaire", readonly=True)  # salaire de base des fonctionnaires
    x_solde_indiciaire_net = fields.Float(string="Salaire de base",
                                          readonly=True)  # salaire de base des fonctionnaires + montant residence
    x_indice = fields.Float(string='Indice')
    # Situation administrative de l'agent dans l'EPE
    x_categorie_c_id = fields.Many2one('hr_categorie', string='Catégorie', required=False)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=False)
    x_echellon_c_id = fields.Many2one('hr_echellon', required=False, string='Echelon')
    # cALCUL DE L'EMOLUMENT
    x_emolument_ctrct = fields.Float(string="Emolument Brut")
    x_taux_retenu_emolmt = fields.Float(string="Taux retenue (%)")
    x_mnt_taux_retenu_emolmt = fields.Float(string="Montant Taux")
    x_emolument_ctrct_net = fields.Float(string="Emolument Net", readonly=True)
    # salaire de base des contractuels
    x_solde_indiciaire_ctrct = fields.Float(string="Salaire de base", required=True)
    #
    date_embauche = fields.Date(string="Date d'embauche", default=date.today())
    date_fin_embauche = fields.Date(string="Date fin")
    date_modiff = fields.Date(string='Date effet', default=date.today())

    #
    type_id = fields.Many2one(comodel_name='hr_contract_type', string='Type contrat')
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)
    struct_id = fields.Many2one("hr.payroll.structure", string="Salary Structure")
    x_emploi_id = fields.Many2one("hr_emploi", string="Emploi", required=True,
                                  default=lambda self: self.env['hr_emploi'].search([('name', '=', 'Choisir Emploi')]))
    x_fonction_id = fields.Many2one("hr_fonctionss", string="Fonction", required=True,
                                    default=lambda self: self.env['hr_fonctionss'].search(
                                        [('name', '=', 'Choisir Fonction')]))
    hr_service = fields.Many2one("hr_service", string="Service")
    x_unite_id = fields.Many2one("hr_unite", string="Unite", required=True)
    x_zone_id = fields.Many2one("hr_zone", string="Zone", required=True)
    x_mode_paiement = fields.Selection([
        ('billetage', 'Billetage'),
        ('virement', 'Virement'),
    ], string="Mode de Paiement", default='billetage', required=True)
    num_banque = fields.Char('N° compte bancaire', required=True)
    x_banque_id = fields.Many2one('res.bank', 'Banque', required=True)
    intitule = fields.Char(string="Intitulé du compte")

    # Salaire de base
    x_salaire_base = fields.Float(string="Salaire de base", required=True)
    x_total_indemnites = fields.Float(string="Total Indemn", readonly=True)
    x_remuneration_total = fields.Float("Rémunération totale", readonly=True)

    # Declaration variables Indemnités
    x_indem_resp = fields.Float(string="Indemn.Resp", readonly=False)
    x_indem_astr = fields.Float(string="Indemn.Astreinte", readonly=False)
    x_indem_techn = fields.Float(string="Indemn.Technicité", readonly=False)
    x_indem_specif = fields.Float(string="Indemn.Spécifique GRH", readonly=False)
    x_indem_loge = fields.Float(string="Indemn.Logement", readonly=False)
    x_indem_transp = fields.Float(string="Indemn.Transport", readonly=False)
    x_indem_inform = fields.Float(string="Indemn.Informatique", readonly=False)
    x_indem_exploit = fields.Float(string="Indemn.Exploitation-Réseau", readonly=False)
    x_indem_finance = fields.Float(string="Indemn.Resp.Financière", readonly=False)
    x_indem_garde = fields.Float(string="Indemn.Garde", readonly=False)
    x_indem_risque = fields.Float(string="Indemn.Risque.Contagion", readonly=False)
    x_indem_suj = fields.Float(string="Indemn.Sujétion Géographique", readonly=False)
    x_indem_form = fields.Float(string="Indemn.Formation", readonly=False)
    x_indem_caisse = fields.Float(string="Indemn.Caisse", readonly=True)
    x_indem_veste = fields.Float(string="Indemn.Vestimentaire", readonly=True)
    x_indem_spec_inspect_trav = fields.Float(string="Indemn.Spécifique Inspecteur de Travail", readonly=True)
    x_indem_spec_inspect_ifc = fields.Float(string="Indemn.Spécifique Forfaitaire Compensatrice", readonly=True)
    x_indem_spec_inspect_irp = fields.Float(string="Indemn.Spécifique de Responsabilité Pécunière", readonly=True)
    x_indem_spec_inspect_ish = fields.Float(string="Indemn.Spécifique Harmonisée Personnel MENA et MESRSI",
                                            readonly=True)
    x_indem_prime_rendement = fields.Float(string="Prime rendement", readonly=True)
    x_indemnite_residence = fields.Float(string='Indemnité de residence')

    # Affectation du solde indiciaire et calcul du salaire de base fonctionnaire
    @api.onchange('x_echellon_id', 'x_classees_id', 'x_echelle_id', 'x_categorie_id')
    def sal_base(self):
        val_class = int(self.x_classees_id)
        val_echel = int(self.x_echelle_id)
        val_echellon = int(self.x_echellon_id)
        val_cat = int(self.x_categorie_id)
        if val_class != False and val_echel != False and val_echellon != False and val_cat != False:
            res = self.env['hr_grillesalariale'].search(
                [('x_echellon_id', '=', val_echellon), ('x_class_id', '=', val_class), ('x_categorie_id', '=', val_cat),
                 ('x_echelle_id', '=', val_echel)])
            self.x_solde_indiciaire = round(res.x_salbase)  # x_salbase=solde indiciaire
            self.x_indemnite_residence = round((res.x_salbase * 10 / 100) + 0.1)  # 0.1:permet de mieux arrondir
            self.x_solde_indiciaire_net = self.x_solde_indiciaire + self.x_indemnite_residence  # solde indiciaire_net= salaire de base
            self.x_indice = round(res.x_indice)

    # fonction de recherche permettant de retourner le salaire de base dans la grille des contractuels en fonction des paramètres
    @api.onchange('x_echellon_c_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def sal_basec(self):
        val_echel_c = int(self.x_echelle_c_id)
        val_echellon_c = int(self.x_echellon_c_id)
        val_struct = int(self.company_id.id)
        val_cat_c = int(self.x_categorie_c_id)
        if val_echel_c != False and val_echellon_c != False and val_cat_c != False and val_struct != False:
            res = self.env['hr_grillesalariale_contractuel'].search(
                [('x_echellon_c_id', '=', val_echellon_c), ('x_categorie_c_id', '=', val_cat_c),
                 ('x_echelle_c_id', '=', val_echel_c), ('company_id', '=', val_struct)])
            self.x_solde_indiciaire_ctrct = round(res.x_salbase_ctrt)

    # Affectation
    @api.onchange('x_solde_indiciaire', 'x_solde_indiciaire_ctrct', 'struct_id')
    def sal_base_c_f(self):
        for rec in self:
            print("==MAX")
            print(rec.struct_id)
            if rec.struct_id.id == 1:
                rec.x_salaire_base = rec.x_solde_indiciaire_net
            if rec.struct_id.id == 2:
                rec.x_salaire_base = rec.x_solde_indiciaire_ctrct

    # fonction qui permet d'additionner les indemnités
    @api.onchange('x_indem_resp', 'x_indem_astr', 'x_indem_techn', 'x_indem_specif', 'x_indem_spec_inspect_trav',
                 'x_indem_spec_inspect_irp', 'x_indem_spec_inspect_ish', 'x_indem_spec_inspect_ifc', 'x_indem_loge',
                 'x_indem_transp', 'x_indem_inform', 'x_indem_exploit', 'x_indem_finance', 'x_indem_garde',
                 'x_indem_risque', 'x_indem_suj', 'x_indem_form', 'x_indem_caisse', 'x_solde_indiciaire',
                 'x_indem_prime_rendement')
    def depend_field(self):
        for val in self:
            val.x_total_indemnites = round(
                val.x_indem_resp + val.x_indem_astr + val.x_indem_techn + val.x_indem_specif + val.x_indem_spec_inspect_trav + val.x_indem_spec_inspect_irp + val.x_indem_spec_inspect_ish + val.x_indem_spec_inspect_ifc + val.x_indem_loge + val.x_indem_transp + val.x_indem_inform + val.x_indem_exploit + val.x_indem_finance + val.x_indem_garde + val.x_indem_risque + val.x_indem_suj + val.x_indem_form + val.x_indem_caisse + val.x_indem_prime_rendement)

