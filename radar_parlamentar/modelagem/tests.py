# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Eduardo Hideo, Diego Rabatone
#
# This file is part of Radar Parlamentar.
#
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from django.test import TestCase
from importadores import convencao
from datetime import date
import models

class ModelsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        importer = convencao.ImportadorConvencao()
        importer.importar()

    def test_partido(self):
        pt = models.Partido.from_nome('PT')
        self.assertEquals(pt.numero, 13)
        psdb = models.Partido.from_numero(45)
        self.assertEquals(psdb.nome, 'PSDB')
        
    def test_partido_from_nome_None(self):
        nome = None
        partido = models.Partido.from_nome(nome)
        self.assertIsNone(partido)

    def test_casa_legislativa_partidos(self):
        conv = models.CasaLegislativa.objects.get(nome_curto='conv')
        partidos = conv.partidos()
        self.assertEquals(len(partidos), 3)
        nomes = [ p.nome for p in partidos ]
        self.assertTrue(convencao.JACOBINOS in nomes)
        self.assertTrue(convencao.GIRONDINOS in nomes)
        self.assertTrue(convencao.MONARQUISTAS in nomes)

    def test_casa_legislativa_periodos(self):
        conv = models.CasaLegislativa.objects.get(nome_curto='conv')
        periodos = conv.periodos(models.ANO)
        self.assertEquals(len(periodos), 1)
        self.assertEqual(periodos[0].string, '1989')
        self.assertEqual(periodos[0].quantidade_votacoes,8)
        periodos = conv.periodos(models.MES)
        self.assertEquals(len(periodos), 9)
        self.assertEqual(periodos[0].string, '1989 Fev')
        self.assertEqual(periodos[0].quantidade_votacoes,4)
        self.assertEqual(periodos[1].string, '1989 Mar')
        self.assertEqual(periodos[1].quantidade_votacoes,0)
        periodos = conv.periodos(models.SEMESTRE)
        self.assertEquals(len(periodos), 2)
        d = periodos[0].ini
        self.assertEqual(1989, d.year)
        self.assertEqual(1, d.month)
        d = periodos[0].fim
        self.assertEqual(1989, d.year)
        self.assertEqual(6, d.month)
        d = periodos[1].ini
        self.assertEqual(1989, d.year)
        self.assertEqual(7, d.month)
        d = periodos[1].fim
        self.assertEqual(1989, d.year)
        self.assertEqual(12, d.month)
        self.assertEqual(periodos[0].string, '1989 1o Semestre')
        self.assertEqual(periodos[1].string, '1989 2o Semestre')
        periodos = conv.periodos(models.MES,minimo=0.2)
        self.assertEqual(len(periodos),2)
        
    def test_sould_find_legislatura(self):
        dt = date(1989, 07, 14)
        try:
            leg = models.Legislatura.find(dt, 'Pierre')
            self.assertTrue(leg != None)
        except ValueError:
            self.fail('Legislatura não encontrada')
            
    def test_sould_not_find_legislatura(self):
        dt = date(1900, 07, 14)
        try:
            models.Legislatura.find(dt, 'Pierre')
            self.fail('Legislatura não deveria ter sido encontrada')
        except:
            self.assertTrue(True)
            