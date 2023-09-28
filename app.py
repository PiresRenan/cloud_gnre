import os
from datetime import datetime

from flask import Flask, render_template, request, flash, url_for, redirect, jsonify

from gerador_de_lotes_gnre import main
from model.forms import DateFormForGNRE, GNREUnico
from services.alerts import OutlookMailSender

app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candide.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/gnre_em_lote', methods=["GET", "POST"])
def gnre_lote():
    form = DateFormForGNRE(request.form)
    if form.validate_on_submit():
        if request.method == "POST":
            data_inicio = datetime.strptime(form.start_date.data.strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_termino = datetime.strptime(form.end_date.data.strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_atual = datetime.now()
            if data_inicio == '':
                flash('A data de início não pode ficar vazia!', 'error')
                return redirect(url_for('gnre'))
            elif data_inicio > data_termino:
                flash('A data de início não pode ser maior que a data de término', 'error')
                return render_template('gnre_em_lote.html', form=form)
            elif data_termino > data_atual:
                flash(f'A data final não deverá ser posterior a data de hoje ({data_atual.strftime("%d/%m/%Y")}).',
                      'error')
                return render_template('gnre_em_lote.html', form=form)
            else:
                data_inicio = data_inicio.strftime('%d/%m/%Y')
                data_termino = data_termino.strftime('%d/%m/%Y')
                obj_creator = main.Gerador()
                xml_builded = obj_creator.criar_guias_em_lote(data_inicio, data_termino)
                if not xml_builded == 'Inexistente':
                    flash('GNRE gerada com sucesso!', 'success')
                    temp_dir = './temp'
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)
                    gnre_file = os.path.join(temp_dir, 'gnre.xml')
                    with open(gnre_file, 'w') as r:
                        r.write(xml_builded)
                    obj_sender = OutlookMailSender('1')
                    obj_sender.send_gnre()
                    return render_template('gnre_em_lote.html', form=form)
                else:
                    flash('Sem novas notas!', 'error')
                    return render_template('gnre_em_lote.html', form=form)

    return render_template('gnre_em_lote.html', form=form)


@app.route('/gnre_exclusiva', methods=["GET", "POST"])
def gnre_exclusiva():
    form = GNREUnico(request.form)
    if form.validate_on_submit():
        nfe_n = form.nf_number.data
        obj_creator = main.Gerador()
        xml_builded_ = obj_creator.criar_unique(nfe_n)
        if not xml_builded_ == 'Inexistente':
            flash('GNRE gerada com sucesso!', 'success')
            temp_dir = './temp'
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            gnre_file = os.path.join(temp_dir, 'gnre.xml')
            with open(gnre_file, 'w') as r:
                r.write(xml_builded_)
            obj_sender = OutlookMailSender('1')
            obj_sender.send_gnre()
            return render_template('gnre_singular.html', form=form)
        else:
            flash('Sem novas notas!', 'error')
            render_template('gnre_singular.html', form=form)
    return render_template('gnre_singular.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
