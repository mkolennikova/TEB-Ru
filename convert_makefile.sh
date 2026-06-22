#!/bin/bash

# Full script to convert Makefile so that all object files and modules
# are placed into a separate 'obj' directory.
# Works in Linux / Google Colab.

set -e

MAKEFILE="Makefile"
BACKUP="${MAKEFILE}.bak"
OBJDIR="obj"

echo "=== Converting Makefile to build into $OBJDIR directory ==="

# 1. Create a backup
if [ -f "$MAKEFILE" ]; then
    cp "$MAKEFILE" "$BACKUP"
    echo "Backup created: $BACKUP"
else
    echo "Error: file $MAKEFILE not found!"
    exit 1
fi

# 2. Remove all old compilation command lines (starting with tab and $(FC))
sed -i '/^[[:space:]]*$(FC)/d' "$MAKEFILE"
echo "Removed old compilation commands."

# 3. Add OBJDIR variable and directory creation after the include line
sed -i "/^include gfortran_args/a OBJDIR = $OBJDIR\n\$(shell mkdir -p \$(OBJDIR))" "$MAKEFILE"
echo "Added OBJDIR and mkdir."

# 4. Redefine OBJ list with prefix $(OBJDIR)/
# Find the line "OBJ = ..." and replace it with "OBJ = $(addprefix $(OBJDIR)/, ...)"
sed -i 's/^OBJ = /OBJ = \$(addprefix \$(OBJDIR)\/, /' "$MAKEFILE"
# Add closing parenthesis at the end of the OBJ line
sed -i '/^OBJ = \$(addprefix .*/ s/$/)/' "$MAKEFILE"
echo "Updated OBJ list with path to $OBJDIR."

# 5. Append generic build rules and vpath to the end of Makefile
# Use printf to properly insert a tab before commands
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

# 6. Fix the driver1.exe rule
sed -i '/^driver1.exe:/c driver1.exe: $(OBJ) | $(OBJDIR)' "$MAKEFILE"
# Insert the linking command with a tab
sed -i '/^driver1.exe:.*/a \\t$(LD) $(OBJ) -o driver1.exe $(LDFLAGS)' "$MAKEFILE"

# 7. Update clean: add removal of the obj directory
sed -i '/^clean:/a \\t-rm -rf $(OBJDIR)' "$MAKEFILE"

echo "Added generic compilation rules, fixed driver1.exe and clean."

# 8. Add module flags to gfortran_args if not already present
if grep -q "\-J\$(OBJDIR)" gfortran_args; then
    echo "Flag -J already present in gfortran_args."
else
    sed -i '/^FFLAGS = .*gfortran/s/$/ -J$(OBJDIR)/' gfortran_args
    echo "Added -J$(OBJDIR) flag to gfortran_args for gfortran."
fi

if grep -q "\-module \$(OBJDIR)" gfortran_args; then
    echo "Flag -module already present in gfortran_args."
else
    sed -i '/^FFLAGS = .*ifort/s/$/ -module $(OBJDIR)/' gfortran_args
    echo "Added -module $(OBJDIR) flag to gfortran_args for ifort."
fi

echo "=== Conversion completed! ==="
echo "Run 'make clean && make' to build."
echo "Backup file: $BACKUP"