from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from flask_migrate import Migrate
import os

# ---------------- APP ----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ---------------- LOGIN ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---------------- MODELS ----------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    objective = db.Column(db.Text)
    name = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(200))
    education = db.Column(db.String(300))
    technical_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    profile = db.Column(db.Text)
    declaration = db.Column(db.Text)
    place = db.Column(db.String(100))
    date = db.Column(db.String(50))

    user = db.relationship('User', backref=db.backref('resumes', lazy=True))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password']
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully")
        return redirect(url_for('login'))

    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        user = User.query.filter_by(email=request.form['email']).first()

        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard'))

        flash("Invalid login")

    return render_template("login.html")


@app.route('/dashboard')
@login_required
def dashboard():

    resumes = Resume.query.filter_by(user_id=current_user.id).all()

    return render_template("dashboard.html", resumes=resumes)


@app.route('/education', methods=['GET', 'POST'])
@login_required
def education():

    if request.method == 'POST':

        resume = Resume(
            user_id=current_user.id,
            objective=request.form.get('objective', ''),
            name=request.form.get('full_name', ''),
            email=request.form.get('email', ''),
            phone=request.form.get('phone', ''),
            linkedin=request.form.get('linkedin', ''),
            education=request.form.get('education', ''),
            technical_skills=request.form.get('technical_skills', ''),
            soft_skills=request.form.get('soft_skills', ''),
            experience=request.form.get('experience', ''),
            profile=request.form.get('profile', ''),
            declaration=request.form.get('declaration', ''),
            place=request.form.get('place', ''),
            date=request.form.get('date', '')
        )

        db.session.add(resume)
        db.session.commit()

        return redirect(url_for('preview_resume', resume_id=resume.id))

    return render_template("education.html")


@app.route('/preview/<int:resume_id>')
@login_required
def preview_resume(resume_id):

    resume = Resume.query.get_or_404(resume_id)

    if resume.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('dashboard'))

    return render_template("preview_resume.html", resume=resume)


@app.route('/download/<int:id>')
@login_required
def download(id):

    resume = Resume.query.get_or_404(id)

    if resume.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('dashboard'))

    filename = f"resume_{resume.id}.pdf"
    filepath = os.path.join("static", filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4)

    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=8,
        textColor=colors.HexColor('#1f3c88'),
        fontName='Helvetica-Bold'
    )

    elements = []

    # NAME
    elements.append(Paragraph(resume.name or "Your Name", styles['Title']))
    elements.append(Spacer(1, 15))

    # OBJECTIVE
    if resume.objective:
        elements.append(Paragraph("Objective", heading_style))
        elements.append(Paragraph(resume.objective, styles['Normal']))

    # CONTACT
    elements.append(Paragraph("Contact Information", heading_style))
    elements.append(Paragraph(f"<b>Email:</b> {resume.email or ''}", styles['Normal']))
    elements.append(Paragraph(f"<b>Phone:</b> {resume.phone or ''}", styles['Normal']))

    if resume.linkedin:
        elements.append(Paragraph(f"<b>LinkedIn:</b> {resume.linkedin}", styles['Normal']))

    # PROFILE
    if resume.profile:
        elements.append(Paragraph("Profile Summary", heading_style))
        elements.append(Paragraph(resume.profile, styles['Normal']))

    # EDUCATION
    if resume.education:
        elements.append(Paragraph("Education", heading_style))
        elements.append(Paragraph(resume.education, styles['Normal']))

    # EXPERIENCE
    if resume.experience:
        elements.append(Paragraph("Experience", heading_style))
        elements.append(Paragraph(resume.experience, styles['Normal']))

    # TECHNICAL SKILLS
    if resume.technical_skills:
        elements.append(Paragraph("Technical Skills", heading_style))
        elements.append(Paragraph(resume.technical_skills.replace(',', ', '), styles['Normal']))

    # SOFT SKILLS
    if resume.soft_skills:
        elements.append(Paragraph("Soft Skills", heading_style))
        elements.append(Paragraph(resume.soft_skills.replace(',', ', '), styles['Normal']))

    # DECLARATION
    if resume.declaration:
        elements.append(Paragraph("Declaration", heading_style))
        elements.append(Paragraph(resume.declaration, styles['Normal']))

        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Place:</b> {resume.place or ''}", styles['Normal']))
        elements.append(Paragraph(f"<b>Date:</b> {resume.date or ''}", styles['Normal']))

    doc.build(elements)

    return send_file(filepath, as_attachment=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# ---------------- RUN ----------------
if __name__ == "__main__":

    if not os.path.exists("static"):
        os.makedirs("static")

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8000)