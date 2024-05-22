#include "run_dynamic_size.h"

int main() {
  // This SYM_ASSERTs on failure instead of CHECK, since it isn't a test
  robot_3d_localization::RunDynamic();
}
