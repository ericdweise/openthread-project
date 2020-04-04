import statistics


def parse_line(line):
    try:
        fields = line.split(' ')
        packet_size = fields[0]
        trip_time = int(fields[-1].split('=')[1].strip('ms'))
        return packet_size, trip_time
    except:
        raise Exception(f'FAIL ON LINE: "{line}"')


def parse_file(file_name):
    parse_vals = {}

    with open(file_name, 'r') as fin:
        for line in fin:
            if 'bytes' not in line:
                continue

            packet_size, trip_time = parse_line(line.strip())

            if packet_size not in parse_vals.keys():
                parse_vals[packet_size] = []

            parse_vals[packet_size].append(trip_time)

    return parse_vals


def stats(parse_vals):
    results = {}

    for k in parse_vals.keys():
        mean = statistics.mean(parse_vals[k])

        if len(parse_vals[k]) > 1:
            stdev = statistics.stdev(parse_vals[k])
        else:
            stdev = 0

        results[k] = {
                'mean': mean,
                'stdev': stdev,
                'pdr': f'{len(parse_vals[k])}%'}

    return results


def write_results(results, out_file):
    with open(out_file, 'w') as fout:
        fout.write(f'Packet Size,Mean Time,Std Dev,PDR\n')
        for k in results:
            m = results[k]['mean']
            s = results[k]['stdev']
            p = results[k]['pdr']
            fout.write(f'{k},{m},{s},{p}\n')


def main(in_file, out_file):
    print(f'  Parsing {in_file}')
    parse_vals = parse_file(in_file)
    print(parse_vals)
    results = stats(parse_vals)
    write_results(results, out_file)


if __name__ == '__main__':
    main('experiment-results-1-hop.txt', 'outputs-1-hop.csv')
    main('experiment-results-2-hop.txt', 'outputs-2-hop.csv')
    main('experiment-results-3-hop.txt', 'outputs-3-hop.csv')
    main('experiment-results-4-hop.txt', 'outputs-4-hop.csv')
