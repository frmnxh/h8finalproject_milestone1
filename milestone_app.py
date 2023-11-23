from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Milestone API', description='API untuk mencatat milestone')

# Model untuk milestone
milestone_model = api.model('Milestone', {
    'id': fields.Integer(readonly=True, description='ID Milestone'),
    'title': fields.String(required=True, description='Judul Milestone'),
    'description': fields.String(description='Deskripsi Milestone'),
    'status': fields.String(required=True, description='Status Milestone (ongoing/completed)'),
})

# Data dummy sebagai contoh
milestones = [
    {'id': 1, 'title': 'Milestone 1', 'description': 'Deskripsi Milestone 1', 'status': 'ongoing'},
    {'id': 2, 'title': 'Milestone 2', 'description': 'Deskripsi Milestone 2', 'status': 'completed'},
]

# Resource untuk daftar milestones dan pembuatan baru
@api.route('/milestones')
class MilestoneListResource(Resource):
    @api.marshal_list_with(milestone_model)
    def get(self):
        return milestones

    @api.expect(milestone_model)
    @api.marshal_with(milestone_model, code=201)
    def post(self):
        data = api.payload
        new_milestone = {
            'id': len(milestones) + 1,
            'title': data['title'],
            'description': data.get('description', ''),
            'status': data['status'],
        }
        milestones.append(new_milestone)
        return new_milestone, 201

# Resource untuk operasi CRUD pada milestone tertentu
@api.route('/milestones/<int:milestone_id>')
class MilestoneResource(Resource):
    @api.marshal_with(milestone_model)
    def get(self, milestone_id):
        milestone = next((m for m in milestones if m['id'] == milestone_id), None)
        if milestone:
            return milestone
        api.abort(404, message=f'Milestone dengan ID {milestone_id} tidak ditemukan')

    @api.expect(milestone_model)
    @api.marshal_with(milestone_model)
    def put(self, milestone_id):
        milestone = next((m for m in milestones if m['id'] == milestone_id), None)
        if milestone:
            data = api.payload
            milestone.update(data)
            return milestone
        api.abort(404, message=f'Milestone dengan ID {milestone_id} tidak ditemukan')

    def delete(self, milestone_id):
        global milestones
        milestones = [m for m in milestones if m['id'] != milestone_id]
        return '', 204

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)
