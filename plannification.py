import pandas
from infrastructure import Infrastructure
from building import Building

class Planification:
	def __init__(self, csv_path):
		self.csv_path = csv_path

	def prepare_data(self):
		network_df = pandas.read_csv(self.csv_path)
		network_df = network_df[network_df["infra_type"] == "a_remplacer"]
		

		dict_infra = {}
		infra_subdfs = network_df.groupby("infra_id")
		for infra_id, infra_subdf in infra_subdfs:
			length = infra_subdf["longueur"].iloc[0]
			infra_type = infra_subdf["infra_type"].iloc[0]
			nb_houses = infra_subdf["nb_maisons"].sum()
			dict_infra[infra_id] = Infrastructure(infra_id, length, infra_type, nb_houses)


		list_building = []	
		building_subdfs = network_df.groupby("id_batiment")
		for id_building, building_subdf in building_subdfs:
			list_infra = [dict_infra[infra_id] for infra_id in building_subdf["infra_id"]]
			list_building.append(Building(id_building, list_infra))

		return list_building

	def run_planification_algo(self, list_building):
		sorted_buildings = []
		while list_building:
			
			easiest_building = min(list_building)
			for infra_object in easiest_building.list_infras:
				infra_object.repair_infra()

			sorted_buildings.append(easiest_building)
			list_building.remove(easiest_building)


		return sorted_buildings


	def show_exports_for_datavisulation(self, sorted_buildings):
		sorted_buildings_ids = [building_object.id_building for building_object in sorted_buildings]

		sorted_infras_ids = []
		for building in sorted_buildings:
			for infra_object in building.list_infras:
				if infra_object.infra_id not in sorted_infras_ids:
					sorted_infras_ids.append(infra_object.infra_id)

		pandas.DataFrame({"building_id": sorted_buildings_ids,\
						  "index_priority":[index for index in range(len(sorted_buildings))]}).to_excel("./building_priority.xlsx", index=False)


		pandas.DataFrame({"infra_id": sorted_infras_ids,\
						  "index_priority":[index for index in range(len(sorted_infras_ids))]}).to_excel("./infra_priority.xlsx", index=False)


if __name__ == "__main__":
	csv_path = "../data/reseau_en_arbre.csv"
	planification_object = Planification(csv_path)

	list_building = planification_object.prepare_data()
	
	sorted_buildings = planification_object.run_planification_algo(list_building)

	planification_object.show_exports_for_datavisulation(sorted_buildings)