from .entities.Disp import Disp
from flask import flash
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError

class ModelDisp():

#metodo para obtener un dispositivo
    @classmethod
    def get_disps(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "Select alias, name, dir_mac from dispositivos"
            cursor.execute(sql)
            results = cursor.fetchall()
            disps = []
            i = 1
            for row in results:
                result_dict = {
                    "id": i,
                    "alias": row[0],
                    "name": row[1],
                    "dir_mac": row[2]
                }
                disps.append(result_dict)
                i += 1

            return disps
        except Exception as ex:
            raise Exception(ex)
    
#metodo para insertar dispositivos
    @classmethod
    def insert_disps(self, db, disp: Disp):
        try:
            cursor = db.connection.cursor()
            sql = f"INSERT INTO `dispositivos`(`alias`, `name`, `dir_mac`) VALUES ('{disp.alias}','{disp.name}','{disp.mac}')"
            cursor.execute(sql)
            db.connection.commit()
        except IntegrityError as ex:
            if "Duplicate entry" in str(ex):
                flash("Este dispositivo ya está registrado.", "error")
            else:
                flash(str(ex), "error")
        except Exception as ex:
            raise Exception(ex)

            

#metodo para borrar dispositivos
    @classmethod
    def del_disps(self, db, mac):
        try:
            cursor = db.connection.cursor()
            sql = f"delete from dispositivos where dir_mac like '{mac}'"
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)