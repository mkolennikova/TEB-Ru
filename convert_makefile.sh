#!/bin/bash

# Script to convert Makefile: place all objects and modules into 'obj/'
# Works in Linux / Google Colab.

set -e

MAKEFILE="Makefile"
BACKUP="${MAKEFILE}.bak"
OBJDIR="obj"

echo "=== Converting Makefile to build into $OBJDIR directory ==="

# 1. Backup
if [ -f "$MAKEFILE" ]; then
    cp "$MAKEFILE" "$BACKUP"
    echo "Backup created: $BACKUP"
else
    echo "Error: $MAKEFILE not found!"
    exit 1
fi

# 2. Remove old compilation commands (lines starting with tab and $(FC))
sed -i '/^[[:space:]]*$(FC)/d' "$MAKEFILE"
echo "Removed old compilation commands."

# 3. Add OBJDIR and mkdir after include
sed -i "/^include gfortran_args/a OBJDIR = $OBJDIR\n\$(shell mkdir -p \$(OBJDIR))" "$MAKEFILE"
echo "Added OBJDIR and mkdir."

# 4. Redefine OBJ with prefix $(OBJDIR)/
sed -i 's/^OBJ = /OBJ = \$(addprefix \$(OBJDIR)\/, /' "$MAKEFILE"
sed -i '/^OBJ = \$(addprefix .*/ s/$/)/' "$MAKEFILE"
echo "Updated OBJ list with path to $OBJDIR."

# 5. Add module search flags directly in the Makefile (after include)
# Insert the conditional block after the include line
sed -i "/^include gfortran_args/a \\\\n# Add module search path\nifeq (\$(FC),ifort)\n    FFLAGS += -module \$(OBJDIR)\nelse\n    FFLAGS += -J\$(OBJDIR)\nendif" "$MAKEFILE"
echo "Added module search flags to Makefile."

# 6. Remove the localize and copy rules (to avoid circular deps)
# Delete lines from './something: ...' up to the end of that block (simple approach: delete all lines starting with './')
sed -i '/^\.\//d' "$MAKEFILE"
echo "Removed localize/copy rules to avoid circular dependencies."

# 7. Append generic build rules and vpath
cat >> "$MAKEFILE" << 'EOF'

# ----- Automatic rules for building into obj/ -----
vpath %.F90 src_driver src_teb src_struct src_proxi_SVAT src_solar
vpath %.f90 src_driver src_teb src_struct src_proxi_SVAT src_solar
vpath %.F   src_teb
vpath %.f   src_teb

$(OBJDIR)/%.o: %.F90 | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.f90 | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.F | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.f | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@
EOF

# 8. Fix driver1.exe rule
sed -i '/^driver1.exe:/c driver1.exe: $(OBJ) | $(OBJDIR)' "$MAKEFILE"
sed -i '/^driver1.exe:.*/a \\t$(LD) $(OBJ) -o driver1.exe $(LDFLAGS)' "$MAKEFILE"

# 9. Update clean
sed -i '/^clean:/a \\t-rm -rf $(OBJDIR)' "$MAKEFILE"

echo "Added generic compilation rules, fixed driver1.exe and clean."

# 10. Remove any duplicate lines that might have been inserted (optional)
# Not needed for now.

echo "=== Conversion completed! ==="
echo "Run 'make clean && make' to build."
echo "Backup: $BACKUP"