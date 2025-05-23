from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/calculate', methods=['POST'])
def calculate_cgpa():
    if request.method == 'POST':
        try:
            completed_courses = int(request.form['completed_courses'])
            completed_credits = float(request.form['completed_credits'])
            current_cgpa = float(request.form['current_cgpa'])
            total_quality_points = completed_credits * current_cgpa

            course_data = []
            total_new_credits = 0
            total_new_quality_points = 0

            for i in range(int(request.form['current_courses'])):
                is_thesis = request.form.get(f'is_thesis_{i}') == 'yes'
                grade = float(request.form.get(f'grade_{i}'))
                credit = 4 if is_thesis else 3
                total_new_credits += credit
                total_new_quality_points += credit * grade
                course_data.append({'thesis': is_thesis, 'grade': grade, 'credit': credit})

            updated_total_credits = completed_credits + total_new_credits
            updated_total_quality_points = total_quality_points + total_new_quality_points
            new_cgpa = updated_total_quality_points / updated_total_credits

            return render_template('result.html', credits=updated_total_credits, cgpa=round(new_cgpa, 2))
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)