import xml.etree.ElementTree as ET

class Parser:
    def parse_and_extract(filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        namespace = {'ns': 'http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec'}
        def extract_file_header(root, namespace):
            file_header = root.find('ns:fileHeader', namespace)
            file_format_version = file_header.attrib['fileFormatVersion']
            file_sender = file_header.find('ns:fileSender', namespace).text if file_header.find('ns:fileSender',
                                                                                                namespace) is not None else ''
            begin_time = file_header.find('ns:measCollec', namespace).attrib['beginTime']
            return {
                'fileFormatVersion': file_format_version,
                'fileSender': file_sender,
                'beginTime': begin_time
            }

        def extract_meas_data(root, namespace):
            meas_data_list = []
            for meas_data_element in root.findall('ns:measData', namespace):
                managed_element = meas_data_element.find('ns:managedElement', namespace).text if meas_data_element.find(
                    'ns:managedElement', namespace) is not None else ''
                meas_infos = []
                for meas_info in meas_data_element.findall('ns:measInfo', namespace):
                    meas_types = [meas_type.text for meas_type in meas_info.findall('ns:measType', namespace)]
                    meas_values = []
                    for meas_value in meas_info.findall('ns:measValue', namespace):
                        for r in meas_value.findall('ns:r', namespace):
                            meas_values.append({
                                'p': int(r.attrib['p']),
                                'value': r.text
                            })
                    meas_infos.append({
                        'measTypes': meas_types,
                        'measValues': meas_values
                    })
                meas_data_list.append({
                    'managedElement': managed_element,
                    'measInfos': meas_infos
                })
            return meas_data_list

        file_header = extract_file_header(root, namespace)
        meas_data = extract_meas_data(root, namespace)

        data = {
            'fileHeader': file_header,
            'measData': meas_data
        }

        return data
