"""Validate the Gungan race's linked NWN resources without a running server."""
from pathlib import Path
import json,re,struct

ROOT=Path(__file__).resolve().parents[1]

def table(name):
    lines=(ROOT/'sw_2da'/f'{name}.2da').read_text(encoding='utf-8-sig').splitlines()
    columns=lines[2].split()
    return [dict(zip(columns,re.findall(r'"[^"]*"|\S+',line)[1:])) for line in lines[3:] if line.strip()]

def validate():
    race=table('racialtypes')[170]
    assert race['Label']=='Gungan' and race['Appearance']=='10269' and race['PlayerRace']=='1'
    appearance=table('appearance')[10269]
    assert appearance['RACE']=='E' and appearance['MODELTYPE']=='P' and appearance['RACIALTYPE']=='170'
    assert float(appearance['HEIGHT'])<float(table('appearance')[10003]['HEIGHT'])
    for name in ['cls_pres_force', 'cls_pres_stand']:
        assert any(row['ReqType']=='RACE' and row['ReqParam1']=='170' for row in table(name)), name
    tlk=json.loads((ROOT/'sw_tlk/sw_tlk.tlk.json').read_text(encoding='utf-8'))
    entries={row['id']:row['text'] for row in tlk['entries']}
    raw=(ROOT/'sw_tlk/sw_tlk.tlk').read_bytes()
    assert raw[:8]==b'TLK V3.0'
    offset=struct.unpack_from('<I',raw,16)[0]
    for field in ['Name','ConverName','ConverNameLower','NamePlural','Description']:
        idx=int(race[field])-16777216
        entry=20+idx*40
        start,length=struct.unpack_from('<II',raw,entry+28)
        assert raw[offset+start:offset+start+length].decode('cp1252')==entries[idx]
    for sex in 'mf':
        for slot in range(300,305):
            name=f'p{sex}e0_head{slot}'
            raw=(ROOT/'sw_pt_head'/f'{name}.mdl').read_bytes()
            assert raw[:4]==bytes(4),name
            source=(ROOT/'model_sources/gungan'/f'{name}.mdl').read_text()
            assert f'newmodel {name}' in source
            for texture in re.findall(r'^\s*bitmap\s+(\S+)',source,re.M):
                assert (ROOT/'sw_pt_head'/f'{texture}.tga').is_file(),texture
                assert (ROOT/'sw_pt_head'/f'{texture}.tga').read_bytes()[17] & 0x30 == 0, texture
    portraits=[row for row in table('portraits') if row['Race']=='170']
    assert len(portraits)==15
    assert sum(row['Sex']=='0' for row in portraits)==8
    assert sum(row['Sex']=='1' for row in portraits)==7
    for row in portraits:
        for suffix,w,h in [('h',256,512),('l',128,256),('m',64,128),('s',32,64),('t',16,32)]:
            name='po_'+row['BaseResRef']+suffix
            raw=(ROOT/'sw_portrait'/f'{name}.dds').read_bytes()
            assert raw[:4]==b'DDS ' and raw[84:88]==b'DXT1'
            assert struct.unpack_from('<II',raw,12)==(h,w)
            assert struct.unpack_from('<I',raw,28)[0]==1
            assert (ROOT/'sw_portrait'/f'{name}.txi').read_text().strip()=='mipmap 0'
    icon=(ROOT/'sw_ui/ir_gungan.tga').read_bytes()
    assert struct.unpack_from('<HH',icon,12)==(64,64)
    print('PASS: Gungan race/appearance/class/TLK links, 10 compiled heads, 15 portrait sets, and icon.')

if __name__=='__main__':
    validate()
