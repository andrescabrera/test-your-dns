#!/bin/bash

# Check if a file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <dns_list_file>"
    exit 1
fi

DNS_FILE="$1"

# Check if the file exists
if [ ! -f "$DNS_FILE" ]; then
    echo "File not found: $DNS_FILE"
    exit 1
fi

# Function to test a DNS server for 30 seconds
test_dns() {
    local dns_ip=$1
    local duration=10
    local end_time=$((SECONDS + duration))
    local times=()

    echo "Testing DNS: $dns_ip for $duration seconds..."

    while [ $SECONDS -lt $end_time ]; do
        result=$(dig @"$dns_ip" www.google.com | grep "Query time" | awk '{print $4}')
        if [[ -n "$result" ]]; then
            times+=("$result")
        fi
        sleep 2
    done

    if [ ${#times[@]} -eq 0 ]; then
        echo "$dns_ip - FAILED (No response)"
        return
    fi

    # Calculate average
    sum=0
    for t in "${times[@]}"; do
        sum=$((sum + t))
    done
    avg=$((sum / ${#times[@]}))

    echo "$dns_ip - Average Query Time: ${avg}ms"
    echo "$dns_ip,$avg" >> results.csv
}

# Clear previous results
echo "DNS_IP,AVG_TIME" > results.csv

# Test each DNS from the file
while IFS= read -r dns; do
    test_dns "$dns"
done < "$DNS_FILE"

# Find the best DNS
best_dns=$(sort -t, -k2 -n results.csv | head -n 2 | tail -n 1)
echo "Best DNS Server: $best_dns"

