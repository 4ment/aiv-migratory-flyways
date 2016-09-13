import os
import re
import sys

rootDir = '.'

genes = 'PB2', 'PB1', 'PA', 'NP', 'MP'

data = {
    # PB2 36
    'PB2': ('CA', 'NV', 'OR', 'WA', 'AK', 'BC', 'CO', 'TX', 'ND', 'AB', 'SK', 'AL', 'AR', 'IL', 'IA', 'LA', 'MI', 'MN', 'MS', 'MO', 'OH', 'WI', 'ON', 'DE', 'ME', 'MD', 'MA', 'NJ', 'NY', 'NC', 'PA', 'VA', 'QC', 'PE', 'NS', 'NB'),
    # PB1 38
    'PB1': ('CA', 'ID', 'NV', 'OR', 'WA', 'AK', 'BC', 'CO', 'TX', 'ND', 'AB', 'SK', 'AL', 'AR', 'IL', 'IA', 'LA', 'MI', 'MN', 'MS', 'MO', 'OH', 'WI', 'ON', 'DE', 'ME', 'MD', 'MA', 'NJ', 'NY', 'NC', 'PA', 'VA', 'QC', 'PE', 'NS', 'NB', 'NL'),
    # PA 38
    'PA': ('CA', 'OR', 'WA', 'AK', 'BC', 'CO', 'TX', 'SD', 'ND', 'AB', 'SK', 'AL', 'AR', 'IL', 'IA', 'LA', 'MI', 'MN', 'MS', 'MO', 'OH', 'WI', 'ON', 'DE', 'FL', 'ME', 'MD', 'MA', 'NJ', 'NY', 'NC', 'PA', 'VA', 'QC', 'PE', 'NS', 'NB', 'NL'),
    # NP 37
    'NP': ('CA', 'ID', 'OR', 'WA', 'AK', 'BC', 'CO', 'TX', 'ND', 'AB', 'SK', 'AL', 'AR', 'IL', 'IA', 'LA', 'MI', 'MN', 'MS', 'MO', 'OH', 'WI', 'ON', 'DE', 'FL', 'ME', 'MD', 'MA', 'NJ', 'NY', 'NC', 'PA', 'VA', 'QC', 'PE', 'NS', 'NB'),
    # MP 37
    'MP': ('CA', 'NV', 'OR', 'WA', 'AK', 'BC', 'CO', 'TX', 'ND', 'AB', 'SK', 'AL', 'AR', 'IL', 'IA', 'LA', 'MI', 'MN', 'MS', 'MO', 'OH', 'WI', 'ON', 'DE', 'ME', 'MD', 'MA', 'NJ', 'NY', 'NC', 'PA', 'VA', 'QC', 'PE', 'NS', 'NB', 'NL')
}

def parse_countries(path):
    dic = {}
    with open(path) as fp:
        for line in fp:
            line = line.rstrip('\n').rstrip('\r')

            if not line.startswith('State'):
                l = line.split(',')
#                dic[l[1]] = {'flyway': l[2], 'country': l[3], 'fullname': l[0]}
                dic[l[1]] = l[2]
    return dic


def get_flyway_model(fs, stateToFlyway):
    model = ''
    flywayToRateIndex = {}
    for i in range(len(fs)):
        flywayToRateIndex[fs[i]] = {}
        for j in range(len(fs)):
            flywayToRateIndex[fs[i]][fs[j]] = 0

    count = 0
    for i in range(len(fs)):
        flywayToRateIndex[fs[i]][fs[i]] = count
        count += 1
        for j in range(i+1, len(fs)):
            flywayToRateIndex[fs[i]][fs[j]] = flywayToRateIndex[fs[j]][fs[i]] = count
            count += 1

    ss = data[gene]
    for state1 in ss:
        for state2 in ss:
            if state1 == state2:
                model += '0,'
            else:
                model += str(flywayToRateIndex[stateToFlyway[state1]][stateToFlyway[state2]]) + ','
    return model.rstrip(',')


def get_two_rate_model(stateToFlyway):
    model = ''
    ss = data[gene]
    for state1 in ss:
        for state2 in ss:
            if stateToFlyway[state1] == stateToFlyway[state2]:
                model += '0,'
            else:
                model += '1,'
    return model.rstrip(',')


re_state = re.compile(r'^>.+(\w{2})$')

stateTo4Flyway = parse_countries(os.path.join(rootDir, 'countries.csv'))

stateTo3Flyway = stateTo4Flyway.copy()
for state in stateTo3Flyway.keys():
    if stateTo3Flyway[state] == 'Mississippi':
        stateTo3Flyway[state] = 'Central'

fs4 = ['Pacific', 'Central', 'Mississippi', 'Atlantic']
fs3 = ['Pacific', 'Central', 'Atlantic']

for gene in genes:
    sys.stdout.write(gene + '\n')

    sys.stdout.write('Number of states ' + str(len(data[gene])) + '\n')

    sys.stdout.write('4 flyway model:\n\n')
    m = get_flyway_model(fs4, stateTo4Flyway)

    cmd = '~/CProjects/phyloc/phyloc/Release/physher -i ' + os.path.join(rootDir, gene, 'geo.fa') + ' -t ' + os.path.join(rootDir, gene, 'ExaML_result.tree')
    cmd += ' --states ' + ','.join(data[gene]) + ' -m ' + m + ' -F df -o 4flyway'
    sys.stdout.write(cmd + '\n\n')

    sys.stdout.write('3 flyway model:\n\n')
    m = get_flyway_model(fs3, stateTo3Flyway)

    cmd = '~/CProjects/phyloc/phyloc/Release/physher -i ' + os.path.join(rootDir, gene, 'geo.fa') + ' -t ' + os.path.join(rootDir, gene, 'ExaML_result.tree')
    cmd += ' --states ' + ','.join(data[gene]) + ' -m ' + m + ' -F df -o 3flyway'
    sys.stdout.write(cmd + '\n\n')

    sys.stdout.write('2 rate model (4 flyway)\n\n')
    m = get_two_rate_model(stateTo4Flyway)

    cmd = '~/CProjects/phyloc/phyloc/Release/physher -i ' + os.path.join(rootDir, gene, 'geo.fa') + ' -t ' + os.path.join(rootDir, gene, 'ExaML_result.tree')
    cmd += ' --states ' + ','.join(data[gene]) + ' -m ' + m + ' -F df -o 2rate'
    sys.stdout.write(cmd + '\n\n')

    sys.stdout.write('2 rate model (3 flyway)\n\n')
    m = get_two_rate_model(stateTo3Flyway)

    cmd = '~/CProjects/phyloc/phyloc/Release/physher -i ' + os.path.join(rootDir, gene, 'geo.fa') + ' -t ' + os.path.join(rootDir, gene, 'ExaML_result.tree')
    cmd += ' --states ' + ','.join(data[gene]) + ' -m ' + m + ' -F df -o 2rate3'
    sys.stdout.write(cmd + '\n\n')

    sys.stdout.write('\n\n')
