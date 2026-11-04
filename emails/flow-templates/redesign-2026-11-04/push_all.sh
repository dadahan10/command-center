#!/bin/bash
# Push every built template to its flow-message template in Klaviyo (DRAFT flows only) and render it with a real past event.
cd "$(dirname "$0")"
declare -A CTX=( [WtYdde]=checkout [VdW7XY]=checkout [SNvbQS]=checkout [VLjUfd]=checkout [WiHGws]=checkout [V4FBhc]=checkout [TNDw3W]=checkout [SyBqNG]=checkout
 [U58x8u]=cart [UBwjpH]=cart [Xzm3N4]=cart [Y7JQ5h]=cart [WRGJQ3]=cart [TPeL6i]=cart [UmCymx]=cart [XjtgKS]=cart
 [WwmdnE]=viewed [UDi5wM]=viewed [XB8MV8]=viewed [QXP4ar]=viewed
 [WHCJdX]=placed [Xg2wvc]=placed [RCR6Vz]=fulfilled [V4smfK]=delivered [RZYnw2]=delivered [TbpdpS]=delivered [W9dVNd]=delivered [TLpfRY]=placed )
for t in "${!CTX[@]}"; do
  [ -n "$1" ] && [[ " $* " != *" $t "* ]] && continue
  python push.py "$t" "out/$t.html" "contexts/${CTX[$t]}.json"
done
